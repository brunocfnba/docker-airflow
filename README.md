# Running Apache Airflow on Docker Containers

This guide has two sessions, first one on how to setup Airflow using Docker containers on premisses. Second one how to do the same thing on IBM Bluemix. Both a pretty similar but there are some differences.

We'll work with Airflow using the Local Executor option where tasks run in parallel using theads in the same machine. Since this architecture covers our needs here we didn't work with Celery executor to have a more distributed architecture.

The diagram below shows this installation architecture.
<div style="text-align:center"><img src="https://lh4.googleusercontent.com/4GveF69OxQUH2r-5hTWAM-1AEfWOcuxQPbqcaGCPGKr5GtPyhs3Qbb9BFXoJLL0lGrk39d0W3AzXB9g=w2560-h1310-rw" width="400"></div>

I picked PostgreSQL database since it's recommended by the community but there are other options to use.
> SQLLite is the default database used and shipped with Airflow but does not work in Local Executor mode.

> If you want to know more about Airflow and how it works go to the [Airflow Offical Web Site](https://airflow.incubator.apache.org/).

### airflow.cfg settings
The airflow.cfg file is where all the settings used by Airflow are stored. This file is located in the AIRFLOW_HOME where Airflow looks for it after installation.
> All this setup has already been done in the Dockerfiles provided.

##### 1. Database
* Look for the `sql_alchemy_conn = ` line in the airflow.cfg file and replace with the connection string from your datbase following the model provided.
> For more on Airflow and databases: [Airflow Offical Web Site - Configuration](https://airflow.incubator.apache.org/configuration.html).

##### 2. Authentication
* To enable authentication when accessing the UI interface this line in the airflow.cfg file `authenticate = True` must be set to true (already done in the file provided).
* It's also required to run a python script when creating the container so the first user can be created. Other user can be created within the Airflow UI.
  * Edit the `set_auth.py` file and add the desired username, e-mail and password.
> There are other methods of authentication in Airflow like LDAP. I using the web method. Go to [Airflow Offical Web Site - Security](https://airflow.incubator.apache.org/security.html) for more.
