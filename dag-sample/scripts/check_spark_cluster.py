import subprocess
import logging

def check_clusters(**kwargs):

    USER = "<username>"
    HOST="<hostname>"
    
    master_n1 = False
    workers_n1 = False
    workers_n2 = False
    workers_count = 0
    
    #Check Node 1 with Master and 3 Workers
    COMMAND="ksh /home/spark/scripts/get_spark_info_node1.sh"

    ssh = subprocess.Popen(["ssh", "-p 17252", USER + '@' + HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    error = ssh.stderr.readlines()
    
    if error != []:
        raise EnvironmentError("Node 1: " + str(error))
    else:
        for i in result:
            if(i.find('org.apache.spark.deploy.master.Master') != -1):
                master_n1 = True
            if(i.find('org.apache.spark.deploy.worker.Worker') != -1):
                workers_count += 1
        
        #print 'workers_count: {}. Master: {}'.format(workers_count, master_n1)
                
        if(master_n1 and (workers_count == 3)):
            workers_n1 = True
        else:
            return False
        
        
    
    #Check Node 2 with 4 Workers
    COMMAND="ksh /home/spark/scripts/get_spark_info_node2.sh"

    ssh = subprocess.Popen(["ssh", "-p 17252", USER + '@' + HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    error = ssh.stderr.readlines()
    
    if error != [] and error[0] != "Pseudo-terminal will not be allocated because stdin is not a terminal.\r\n":
        raise EnvironmentError("Node 2: " + str(error))
    else:
        workers_count = 0
        for i in result:
            if i.find('org.apache.spark.deploy.worker.Worker') != -1:
                workers_count += 1
        
        #print 'workers_count: {}. Master: {}'.format(workers_count, master_n1)
                
        if workers_count == 4:
            workers_n2 = True
        else:
            return False
        
    if master_n1 and workers_n1 and workers_n2:
        return True
    else:
        return False
