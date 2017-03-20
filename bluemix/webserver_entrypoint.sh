#!/usr/bin/env bash

AIRFLOW_HOME="/home/airflow"

cd $AIRFLOW_HOME

chmod 775 /home/airflow/set_auth.py

python /home/airflow/set_auth.py

airflow initdb

sleep 5

airflow webserver
