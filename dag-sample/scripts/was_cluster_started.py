def is_cluster_started(**kwargs):
    value = kwargs['ti'].xcom_pull(task_ids='start_spark_cluster')
    print 'values: ' + str(value)
    if(value):
        return 'slack_started_cluster_ok'
    else:
        return 'slack_unable_start_cluster'
