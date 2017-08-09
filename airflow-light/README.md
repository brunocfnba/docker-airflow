# Light Versions for Aiflow Images

Due to some restrictions inour enviroment we needed to create a very simple image and then run all the container installation during runtime. I know it's not the best practice since we should do it all within the Dockerfile.

I have created one version for Alpine and one for Ubuntu (In their respective directories) since Alpine does not support some IBM DB2 libraries.

To run your container use the following command:
```
bx ic run -d -p8080:8080 --name airflow-scheduler --env-file env_vars airflow_light
```
>populate you 'env_vars' file with all your credentials. This file is not stored withn the container so you don't expose your info.

>You don't need to expose any ports in case you are running a Airflow Scheduler container

#### The env_vars variables

1. **DB_USER** - your database username;
2. **DB_PWD** - your database password;
3. **DB_HOST** - your database hostname;
4. **DB_PORT** - your database port;
5. **DB_NAME** - your database name;
6. **USE_WEX** - [yes|no], if you use Watson Explorer set to 'yes' so you can provide the WEX server to enable SSH without password from Airflow to the server - If you say 'no' you don't need to specify the other WEX variables;
7. **WEX_HOST** - the WEX server hostname;
8. **WEX_PORT** - the WEX server port;
9. **WEX_USER** - the WEX server username;
10. **WEX_PWD** - the Wex server password;
11. **IS_WEB** - [yes|no], tells airflow if that container should start the Ariflow webserver or scheduler;
12. **DB_TYPE** - [mysql|postgres], tell Airflow which database is being used.
