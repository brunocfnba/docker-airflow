# Running Apache Airflow on Docker Containers

This guide has two sessions, first one on how to setup Airflow using Docker containers on premisses. Second one how to do the same thing on IBM Bluemix. Both a pretty similar but there are some differences.

We'll work with Airflow using the Local Executor option where tasks run in parallel using theads in the same machine. Since this architecture covers our needs here we didn't work with Celery executor to have a more distributed architecture.
