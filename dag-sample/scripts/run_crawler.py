import json
import logging
import subprocess
import time

import ibm_db
import requests

from scripts import check_spark_cluster


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def clean_up_table(process_name):
    table_name = 'maximo_{}'.format(process_name)

    dbname = '<DB Name>'
    host = '<hostname>'
    username = '<username>'
    port = '<port>'
    password = '<Password>'

    conn = ibm_db.connect('DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={};PWD={};'
                          .format(dbname, host, port, username, password), '', '')

    if conn:
        sql = 'truncate table {} immediate'.format(table_name)

        stmt = ibm_db.exec_immediate(conn, sql)

        if stmt:
            return True
        else:
            raise EnvironmentError('Problems during statement execution')
    else:
        raise EnvironmentError('Problems with database connection')


def run_spark_etl(process_name):

    # Check Node 1 with Master and 3 Workers
    command = 'ksh /home/spark/scripts/run_spark_etl_{}.sh 2>&1'.format(process_name)
    user = '<username>'
    host = '<hostname>'

    ssh = subprocess.Popen(["ssh", "-p 17252", user + '@' + host, command],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    # result = ssh.stdout.readlines()
    error_list = []
    error = False

    while ssh.poll() is None:
        l = ssh.stdout.readline()  # This blocks until it receives a newline.
        logging.info('{}'.format(l))
        error_list.append(l)
        if len(error_list) > 100:
            error_list.pop(0)
        if l.find('Traceback') != -1 or l.find('not found') != -1:
            error = True

    if not error:
        return True
    else:
        raise EnvironmentError('Problems running Spark job for {} - Errors: {}'
                               .format(process_name, '\n'.join(error_list)))


def run_clean_etl(proc_name, *args, **kwargs):
    cluster_ok = check_spark_cluster.check_clusters()

    if not cluster_ok:
        logging.warning('Cluster seems to be down, restarting it')
        cluster_started = check_spark_cluster.start_cluster()
        if not cluster_started:
            logging.error('Unable to restart the Spark cluster, stopping operations...')
            raise EnvironmentError('Unable to start cluster')

    logging.info('Spark cluster is up, cleaning {} table'.format(proc_name))

    try:
        clean_success = clean_up_table(proc_name)
    except Exception as env:
        logging.error('Problems cleaning up table for {} - Error: {}'.format(proc_name, str(env)))
        raise EnvironmentError('Problems cleaning up table for {} - Error: {}'.format(proc_name, str(env)))

    if clean_success:
        try:
            logging.info('Table from process {} cleaned successfully, starting spark ETL'.format(proc_name))
            spark_etl_ok = run_spark_etl(proc_name)
        except EnvironmentError as e:
            logging.error('Problems running spark ETL for {} - Error: {}'.format(proc_name, e))
            raise EnvironmentError('Problems running spark ETL for {} - Error: {}'.format(proc_name, e))

    if spark_etl_ok:
        logging.info('Spark ETL for {} finished successfully!'.format(proc_name))
        return True


def get_monitor_conn(crawler_name):

    url_monitor = 'http://<hostanme>:<port>/ESAdmin/api/v10/admin/crawler?method=monitorCollectionCrawler'
    payload_monitor = {'collectionId': '<collection_id>', 'output': 'json', 'api_username': '<api username>',
                       'api_password': '<api password>'}
    headers_all = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Authorization': 'Basic <auth token>'}

    res = requests.post(url_monitor, data=payload_monitor, headers=headers_all)
    res_monitor = json.loads(res.text)

    return [i for i in res_monitor if i['displayName'] == crawler_name][0]


def run_crawler(proc_name, is_delta, wait_time, *args, **kwargs):

    headers_all = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Authorization': 'Basic <auth token>'}

    if is_delta:
        crawler_name = 'MAXIMO_{} - DELTA'.format(proc_name.upper())
    else:
        crawler_name = 'MAXIMO_{}'.format(proc_name.upper())

    res_monitor_json = get_monitor_conn(crawler_name)

    crawler_id = res_monitor_json['sessionId']

    url_stop_crawl = 'http://<hostname>:<port>/ESAdmin/api/v10/admin/crawler?method=stop'
    payload_stop_crawl = {'collectionId': '<collection id>', 'output': 'json', 'api_username': '<api username>',
                          'api_password': '<api password>', 'sessionId': crawler_id}

    url_start_crawl = 'http://<hostname>:<port>/ESAdmin/api/v10/admin/crawler?method=startCrawlerAndCrawl'
    payload_start_crawl = {'collectionId': '<collection id>', 'output': 'json', 'api_username': '<api username>',
                           'api_password': '<api password>', 'sessionId': crawler_id}

    logging.info('Stop {} crawler'.format(proc_name))

    res_stop = requests.post(url_stop_crawl, data=payload_stop_crawl, headers=headers_all)
    if json.loads(res_stop.text)['message'] == 'Successful':

        logging.info('Crawler {} stopped, starting it over...'.format(proc_name))
        res_start = requests.post(url_start_crawl, data=payload_start_crawl, headers=headers_all)

        if json.loads(res_start.text)['message'] == 'Successful':
            logging.info('Crawler {} started successfully'.format(proc_name))

            res_monitor_json = get_monitor_conn(crawler_name)

            crawling_status = res_monitor_json['serverStatus']['server']['statusMessage']

            while crawling_status == 'Crawling':
                logging.info('Crawler {} is running - status: {}'.format(proc_name, crawling_status))

                time.sleep(wait_time)

                res_monitor_json = get_monitor_conn(crawler_name)

                crawling_status = res_monitor_json['serverStatus']['server']['statusMessage']

            if crawling_status == 'Completed':
                logging.info('Crawler {} has finished successfully - status: {}'.format(proc_name, crawling_status))
                return True
            else:
                logging.error('Crawler {} failed - status: {}'.format(proc_name, crawling_status))
                raise EnvironmentError('Crawler {} failed'.format(proc_name))

        else:
            logging.error('Error starting {} crawler'.format(proc_name))
            raise EnvironmentError('Error starting {} crawler'.format(proc_name))
    else:
        logging.error('Error stopping {} crawler'.format(proc_name))
        raise EnvironmentError('Error stopping {} crawler'.format(proc_name))


# print run_spark_etl('problem')
