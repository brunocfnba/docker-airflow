#Airflow Image
FROM ubuntu:16.04

ENV AIRFLOW_HOME /home/airflow

RUN useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow

COPY airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY set_auth.py /home/airflow/set_auth.py
COPY init_ubuntu.sh /home/airflow/init_ubuntu.sh

RUN chown -R airflow: ${AIRFLOW_HOME} && chmod -R 775 ${AIRFLOW_HOME}

EXPOSE 8080

#USER airflow
WORKDIR ${AIRFLOW_HOME}

ENTRYPOINT ["sh", "/home/airflow/init_ubuntu.sh"]
