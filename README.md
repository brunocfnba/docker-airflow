# Running Apache Airflow on Docker Containers

This guide has two sessions, first one on how to setup Airflow using Docker containers on premisses. Second one how to do the same thing on IBM Bluemix. Both a pretty similar but there are some differences.

We'll work with Airflow using the Local Executor option where tasks run in parallel using theads in the same machine. Since this architecture covers our needs here we didn't work with Celery executor to have a more distributed architecture.

I picked PostgreSQL database since it's recommended by the community but there are other options to use.
> SQLLite is the default database used and shipped with Airflow but does not work in Local Executor mode.

> If you want to know more about Airflow and how it works go to the [Airflow Offical Web Site](https://airflow.incubator.apache.org/).

### airflow.cfg settings
The airflow.cfg file is where all the settings used by Airflow are stored. This file is located in the AIRFLOW_HOME where Airflow looks for it after installation.
> All this setup has already been done in the Dockerfiles provided.

##### 1. Authentication
* To enable authentication when accessing the UI interface this line in the airflow.cfg file `authenticate = True` must be set to true (already done in the file provided).
* It's also required to run a python script when creating the container so the first user can be created. Other user can be created within the Airflow UI.
  * Edit the `set_auth.py` file and add the desired username, e-mail and password.
> There are other methods of authentication in Airflow like LDAP. I using the web method. Go to [Airflow Offical Web Site - Security](https://airflow.incubator.apache.org/security.html) for more.

##### 2. SMTP
* Airflow has a feature to send e-mails when different actions happen with DAGs in execution like a task failed, retry or success. To do so, provide the SMTP server information in the airflow.cfg file. Look for the `[smtp]` block.
* For this setup gmail SMTP has been used. Replace the information there with the ones from your SMTP server.


### Running on premisses
Follow these instructions to setup on your own environment.

1. Build the image from Dockerfile
```
docker build -t airflow .
```
> You must run the above command in the same path as you Dockerfile.
> -t defines the image name.

2. Create the respective volumes
* The `/home/airflow/dags` folder should be shared by all containers (webserver and scheduler in this case). Edit the `docker-compose-airflow.yml` file and replace `/your/path` with your local file system path.
* The logs volume was defined since it's not a good practice keep the logs within the container. Feel free to also send them to some cloud storage server.
>View the Logs session in the Airflow Web Site Configuration page for more information.

3. Populate you 'env_vars' file with all your credentials. This file is not stored withn the container so you don't expose your info. To run in docker compose, create two copies of the 'env_vars' file. Name one 'env_vars_web' and the other 'env_vars_scheduler'. <BR>Make sure to set 'yes' for the web airflow container in the IS_WEB parameter and 'no' for the scheduler container.
>The env_vars provides all the info so the script know which kind of container create based on the properties below:
<BR><BR>**DB_USER** - your database username;
<BR>**DB_PWD** - your database password;
<BR>**DB_HOST** - your database hostname;
<BR>**DB_PORT** - your database port;
<BR>**DB_NAME** - your database name;
<BR>**USE_WEX** - [yes|no], if you use Watson Explorer set to 'yes' so you can provide the WEX server to enable SSH without password from Airflow to the server - If you say 'no' you don't need to specify the other WEX variables;
<BR>**WEX_HOST** - the WEX server hostname;
<BR>**WEX_PORT** - the WEX server port;
<BR>**WEX_USER** - the WEX server username;
<BR>**WEX_PWD** - the Wex server password;
<BR>**IS_WEB** - [yes|no], tells airflow if that container should start the Ariflow webserver or scheduler;
<BR>**DB_TYPE** - [mysql|postgres], tell Airflow which database is being used.

3. Run the `docker-compose-airflow.yml` file
```
docker-compose -f docker-compose-airflow.yml up -d
```
> `-f` specifies the yml file name and `-d` to run as a deamon.

4. Check the container are up and running
* Run `docker ps -a` and check there are two containers (airflow-web adn aiflow-scheduler) running.
* You should also be able to access the webserver UI on localhost or if you are using boot2docker use the virtua machine IP address (run `docker-machine ip`) to get that.

### Running on IBM Cloud

IBM Cloud offers Docker containers on Kubernetes, take a look on my repo [Setup Airflow on Kubernetes](https://github.com/brunocfnba/Kubernetes-Airflow) to implement your own!
