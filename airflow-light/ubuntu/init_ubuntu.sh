if [ -e /home/airflow/.entrypoint_check ]
then
  if [ "$IS_WEB" = "yes" ]
  then
    sudo -H -u airflow bash -c 'airflow initdb'

    sudo -H -u airflow bash -c 'sleep 5'
    sudo -H -u airflow bash -c 'python /home/airflow/set_auth.py'

    sudo -H -u airflow bash -c 'airflow webserver'
  else
    sudo -H -u airflow bash -c 'airflow scheduler'
  fi

else
  apt-get update && apt-get install -y \
   wget \
   default-jdk \
   python2.7 \
   vim \
   cron \
   python-dev \
   libkrb5-dev \
   libsasl2-dev \
   libssl-dev \
   libffi-dev \
   build-essential \
   libblas-dev \
   liblapack-dev \
   python-pip \
   apt-utils \
   curl \
   netcat \
   iputils-ping \
   openssh-client \
   python-requests \
   libpq-dev \
   libmysqlclient-dev \
   sshpass \
   sudo

  pip install --upgrade pip

  pip install Cython \
  pytz==2015.7 \
  jinja2==2.8.1 \
  cryptography \
  pyOpenSSL \
  ndg-httpsclient \
  pyasn1 \
  psycopg2 \
  slackclient \
  ibm_db \
  pandas==0.18.1 \
  flask-bcrypt \
  airflow[celery,postgres,hive,hdfs,jdbc,password,mysql]==1.8.0

  rm -rf \
         /var/lib/apt/lists/* \
         /tmp/* \
         /var/tmp/* \
         /usr/share/man \
         /usr/share/doc \
         /usr/share/doc-base

    sudo -H -u airflow bash -c 'touch /home/airflow/.entrypoint_check'

    if [ "$DB_TYPE" = "mysql" ]
    then
        su - airflow >> EOF
        sed -i -e 's/<mysql_db_connection>/sql_alchemy_conn = mysql:\/\/'$DB_USER':'$DB_PWD'@'$DB_HOST':'$DB_PORT'\/'$DB_NAME'/g' /home/airflow/airflow.cfg
        EOF
    else
        su - airflow >> EOF
        sed -i -e 's/<mysql_db_connection>/sql_alchemy_conn = postgresql+psycopg2:\/\/'$DB_USER':'$DB_PWD'@'$DB_HOST':'$DB_PORT'\/'$DB_NAME'/g' /home/airflow/airflow.cfg
        EOF
    fi

    if [ "$USE_WEX" = "yes" ]
    then
        echo "Setup WEX Server Key"
        cd /home/airflow
        sudo -H -u airflow bash -c 'mkdir .ssh'
        sudo -H -u airflow bash -c 'ssh-keygen -f /home/airflow/.ssh/id_rsa -t rsa -N ""'
        sudo -H -u airflow bash -c 'ssh -o "StrictHostKeyChecking no" -o PasswordAuthentication=no '$WEX_USER'@'$WEX_HOST' -p'$WEX_PORT
        sudo -H -u airflow bash -c 'cat .ssh/id_rsa.pub | sshpass -p '$WEX_PWD' ssh '$WEX_USER'@'$WEX_HOST' -p'$WEX_PORT' "cat >> .ssh/authorized_keys"'
    fi

    echo "Setup done!"

    if [ "$IS_WEB" = "yes" ]
    then
      sudo -H -u airflow bash -c 'airflow initdb'

      sudo -H -u airflow bash -c 'sleep 5'
      sudo -H -u airflow bash -c 'python /home/airflow/set_auth.py'

      sudo -H -u airflow bash -c 'airflow webserver'
    else
      sudo -H -u airflow bash -c 'airflow scheduler'
    fi

fi
