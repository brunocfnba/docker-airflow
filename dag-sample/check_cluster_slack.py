import pytz
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.slack_operator import SlackAPIPostOperator
from airflow.operators.subdag_operator import SubDagOperator
from datetime import datetime, timedelta
from scripts import check_spark_cluster, is_cluster_up, start_spark_cluster, was_cluster_started
from run_etl_crawler_slack_complete import sub_dag

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 3, 21, 0, 0),
    'email': ['<email address>'],
    'email_on_failure': True,
    'email_on_retry': True
}

slack_channel = '<slack channel name>'
slack_token = '<slack token>

dag = DAG(
    'check_cluster_slack', default_args=default_args, schedule_interval='0 2 * * 1,2,3,4,5')

check_cluster = PythonOperator(
    task_id='check_servers',
    dag=dag,
    provide_context=True,
    retries=1,
    retry_delay=timedelta(minutes=5),
    python_callable=check_spark_cluster.check_clusters)

branch1 = BranchPythonOperator(
    task_id='branch_check_cluster_up',
    dag=dag,
    provide_context=True,
    python_callable=is_cluster_up.is_cluster_up)

send_slack_cluster_ok = SlackAPIPostOperator(
    task_id='slack_cluster_ok',
    token=slack_token,
    channel=slack_channel,
    username='Airflow Buddy',
    text='Hey, I\'ve just checked your *Spark cluster* on WEX Dev servers and everything is fine!\n'
         'I\'m ready to start running the ETLs and crawlers!\n'
         'Message datetime: {{params.curr_date}}',
    params={'curr_date': str(datetime.now(pytz.timezone('America/Sao_Paulo')))},
    dag=dag
)

send_slack_cluster_start = SlackAPIPostOperator(
    task_id='slack_cluster_start',
    token=slack_token,
    channel=slack_channel,
    username='Airflow Buddy',
    text='Darn... looks like there\'s a problem with our Spark cluster.\n'
         'I\'m restarting it!\n'
         'Message datetime: {{params.curr_date}}',
    params={'curr_date': str(datetime.now(pytz.timezone('America/Sao_Paulo')))},
    dag=dag
)

start_cluster = PythonOperator(
    task_id='start_spark_cluster',
    dag=dag,
    provide_context=True,
    retries=1,
    retry_delay=timedelta(minutes=5),
    python_callable=start_spark_cluster.start_cluster)

branch2 = BranchPythonOperator(
    task_id='branch_started_cluster',
    dag=dag,
    provide_context=True,
    python_callable=was_cluster_started.is_cluster_started)

send_slack_cluster_down = SlackAPIPostOperator(
    task_id='slack_unable_start_cluster',
    token=slack_token,
    channel=slack_channel,
    username='Airflow Buddy',
    text='Sorry guys, I tried more than once but can\'t start that cluster up.\n'
         'You better help me out. Thanks'
         'Message datetime: {{params.curr_date}}',
    params={'curr_date': str(datetime.now(pytz.timezone('America/Sao_Paulo')))},
    dag=dag
)


send_slack_cluster_restarted_ok = SlackAPIPostOperator(
    task_id='slack_started_cluster_ok',
    token=slack_token,
    channel=slack_channel,
    username='Airflow Buddy',
    text='Cluster has been *restarted!*\n'
         'It\'s all fine move forward with your ETLs and Crawlers!\n'
         'Message datetime: {{params.curr_date}}',
    params={'curr_date': str(datetime.now(pytz.timezone('America/Sao_Paulo')))},
    dag=dag
)

run_etl_crawler_cluster_up = SubDagOperator(
  subdag=sub_dag('check_cluster_slack', 'crawler_dag_cluster_up', dag.schedule_interval),
  task_id='crawler_dag_cluster_up',
  dag=dag,
)

run_etl_crawler_cluster_restarted = SubDagOperator(
  subdag=sub_dag('check_cluster_slack', 'crawler_dag_cluster_restarted', dag.schedule_interval),
  task_id='crawler_dag_cluster_restarted',
  dag=dag,
)
    
branch1.set_upstream(check_cluster)                                       
send_slack_cluster_ok.set_upstream(branch1)     
send_slack_cluster_start.set_upstream(branch1)
start_cluster.set_upstream(send_slack_cluster_start)
branch2.set_upstream(start_cluster)
send_slack_cluster_down.set_upstream(branch2)
send_slack_cluster_restarted_ok.set_upstream(branch2)
run_etl_crawler_cluster_up.set_upstream(send_slack_cluster_ok)
run_etl_crawler_cluster_restarted.set_upstream(send_slack_cluster_restarted_ok)
