import subprocess
import logging
import check_spark_cluster


def start_cluster(**kwargs):
    USER = "<username>"
    HOST = "<hostname>"

    workers1 = "stopped"
    master = "stopped"
    workers2 = "stopped"

    # Stop workers from node 1
    COMMAND = "ksh /home/spark/spark-2.0.0-bin-hadoop2.7/sbin/stop-slave.sh"

    ssh = subprocess.Popen(["ssh", "-p 17252", USER + '@' + HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    error = ssh.stderr.readlines()

    if error != []:
        raise EnvironmentError("Problems stopping Workers from Node 1: " + str(error))
    else:
        print "stopped workers on node 1 - " + str(result)
        logging.info("Stopped Workers on Node 1 - " + str(result))
        workers1 = "stopped"

    # Stop workers from node 2
    COMMAND = "ksh /home/spark/scripts/stop_workers_node2.sh"

    ssh = subprocess.Popen(["ssh", "-p 17252", USER + '@' + HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    error = ssh.stderr.readlines()

    if (error != [] and error[0] != "Pseudo-terminal will not be allocated because stdin is not a terminal.\r\n"):
        raise EnvironmentError("Problems stopping Workers from Node 2: " + str(error))
    else:
        print "stopped workers on node 2 - " + str(result)
        logging.info("Stopped Workers on Node 2 - " + str(result))
        workers2 = "stopped"

    # Stop master
    COMMAND = "ksh /home/spark/spark-2.0.0-bin-hadoop2.7/sbin/stop-master.sh"

    ssh = subprocess.Popen(["ssh", "-p 17252", USER + '@' + HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    error = ssh.stderr.readlines()

    if error != []:
        raise EnvironmentError("Problems stopping Master on Node 1: " + str(error))
    else:
        print "stopped master on node 1 - " + str(result)
        logging.info("Stopped master on Node 1 - " + str(result))
        master = "stopped"

    # Starting Master
    COMMAND = "ksh /home/spark/scripts/start_master_node1.sh"

    ssh = subprocess.Popen(["ssh", "-p 17252", USER + '@' + HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    error = ssh.stderr.readlines()

    if error != []:
        raise EnvironmentError("Problems starting Master on Node 1: " + str(error))
    else:
        print "started spark master - " + str(result)
        logging.info("Started Spark Master - " + str(result))
        master = "started"

    # Starting Workers on Node 1
    COMMAND = "ksh /home/spark/scripts/start_workers_node1.sh"

    ssh = subprocess.Popen(["ssh", "-p 17252", USER + '@' + HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    error = ssh.stderr.readlines()

    if error != []:
        raise EnvironmentError("Problems starting Workers on Node 1: " + str(error))
    else:
        print "started workers on node 1 - " + str(result)
        logging.info("Started Workers on Node 1 - " + str(result))
        workers1 = "started"

    # Starting workers on Node 2
    COMMAND = "ksh /home/spark/scripts/start_workers_node2.sh"

    ssh = subprocess.Popen(["ssh", "-p 17252", USER + '@' + HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    error = ssh.stderr.readlines()

    if (error != [] and error[0] != "Pseudo-terminal will not be allocated because stdin is not a terminal.\r\n"):
        raise EnvironmentError("Problems starting Workers on Node 2: " + str(error))
    else:
        print "started workers on node 2 - " + str(result)
        logging.info("Started Workers on Node 2 - " + str(result))
        workers2 = "started"

    if ((master == "started") and (workers1 == "started") and (workers2 == "started") and check_spark_cluster.check_clusters()):
        return True
    else:
        return False
