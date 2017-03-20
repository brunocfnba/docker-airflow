#!/usr/bin/env bash

AIRFLOW_HOME="/home/airflow"

cd $AIRFLOW_HOME

sleep 5

airflow scheduler
