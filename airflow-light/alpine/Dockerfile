#Airflow Light Image
FROM alpine:3.6

ENV AIRFLOW_HOME /home/airflow

RUN cd /home && mkdir airflow && cd airflow \
  && adduser -S airflow -g airflow -s /bin/ash

COPY airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY set_auth.py /home/airflow/set_auth.py
COPY init.sh /home/airflow/init.sh

RUN chown -R airflow: ${AIRFLOW_HOME}

RUN chmod -R 775 ${AIRFLOW_HOME}

EXPOSE 8080

WORKDIR ${AIRFLOW_HOME}

ENTRYPOINT ["sh", "/home/airflow/init.sh"]
