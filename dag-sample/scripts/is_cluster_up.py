def is_cluster_up(**kwargs):
    value = kwargs['ti'].xcom_pull(task_ids='check_servers')
    print 'values: ' + str(value)
    if(value):
        return 'slack_cluster_ok'
    else:
        return 'slack_cluster_start'
