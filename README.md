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

##### 3. SMTP
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

3. Run the `docker-compose-airflow.yml` file
```
docker-compose -f docker-compose-airflow.yml up -d
```
> `-f` specifies the yml file name and `-d` to run as a deamon.

4. Check the container are up and running
* Run `docker ps -a` and check there are two containers (airflow-web adn aiflow-scheduler) running.
* You should also be able to access the webserver UI on localhost or if you are using boot2docker use the virtua machine IP address (run `docker-machine ip`) to get that.

### Running on IBM Bluemix

Bluemix offers Docker containers so you don't have to use your own infrastructure.
I'll walk you through the container creation within Bluemix which slightly differ from the normal one we did previoously.

##### 1. Create Bluemix account and install the required software in your machine to handle docker container
First go to [www.bluemix.net](http://www.bluemix.net) and follow the steps presented there to create your account.

Now access the [Install IBM Plug-in to work with Docker](https://console.ng.bluemix.net/docs/containers/container_cli_cfic_install.html) link and follow all the instructions in order to have your local environment ready.

Use the files in the bluemix folder to run the following

##### 2. Setup docker environment variables
To run `docker-compose` commands in Bluemix, first set some environemnt variables as follows.
* Run `cf ic login` command.
* Copy and paste the three environemnt variables set.
```
export DOCKER_HOST=tcp://containers-api.ng.bluemix.net:8443
export DOCKER_CERT_PATH=...
export DOCKER_TLS_VERIFY=1
```

##### 3. Build the image in Bluemix
Due to some issues found in with Bluemix containers when running the entrypoint, two Dockerfiles were created.
Build both of them.
```
docker build -t airflow-web -f Dockerfile_web .
docker build -t airflow-scheduler -f Dockerfile_scheduler .
```
> You must run the above command in the same path as you Dockerfile.
> -t defines the image name.

##### 4. Create data volumes on Bluemix

To share the volumes among the containers create two data volumes (dags and logs)`
```
cf ic volume create dags
cf ic volume create logs
```
> Since the environment variables have been set, `cf ic` and `docker` can be used interchangeably.

> For more details on managing volumes on Bluemix go to [Creating volumes using the command line](https://console.ng.bluemix.net/docs/containers/container_volumes_cli.html)

##### 5. Run the `bm-docker-compose-airflow.yml` file
```
docker-compose -f bm-docker-compose-airflow.yml up -d
```
> `-f` specifies the yml file name and `-d` to run as a deamon.

##### 4. Check the container are up and running
* Run `docker ps -a` and check there are two containers (airflow-web adn aiflow-scheduler) running.

##### 5. Assign an external IP to the webserver container
Since the container are running on the cloud, an external IP is required to access the webserver.
* Request an IP address
```
cf ic ip request
```
* With the IP, bind it to the webserver container
```
cf ic ip bind <your ip address> airflow-web
```
