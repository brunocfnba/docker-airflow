if [ -e /home/airflow/.entrypoint_check ]
then
  if [ "$IS_WEB" = "yes" ]
  then
    airflow initdb

    sleep 5
    python /home/airflow/set_auth.py

    airflow webserver
  else
    airflow scheduler
  fi

else
  echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" > /etc/apk/repositories
  echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
  echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

  apk --update upgrade

  apk add --no-cache mariadb-dev
  apk add --no-cache dumb-init
  apk add --no-cache musl
  apk add --no-cache linux-headers
  apk add --no-cache build-base
  apk add --no-cache ca-certificates
  apk add --no-cache python2
  apk add --no-cache python2-dev
  apk add --no-cache py-setuptools
  apk add --no-cache openssh
  apk add --no-cache sshpass
  apk add --no-cache libffi-dev
  apk add --no-cache libxml2-dev
  apk add --no-cache libxslt-dev
  apk add --no-cache py-psycopg2
  libc6-compat

  if [[ ! -e /usr/bin/python ]];        then ln -sf /usr/bin/python2.7 /usr/bin/python; fi
  if [[ ! -e /usr/bin/python-config ]]; then ln -sf /usr/bin/python2.7-config /usr/bin/python-config; fi
  if [[ ! -e /usr/bin/easy_install ]];  then ln -sf /usr/bin/easy_install-2.7 /usr/bin/easy_install; fi

  easy_install pip

  pip install --upgrade pip
  pip install Cython pytz==2015.7 jinja2==2.8.1 cryptography pyOpenSSL \
  ndg-httpsclient pyasn1 slackclient ibm_db flask-bcrypt \
  airflow[jdbc,password,mysql,postgres]==1.8.0

  rm -rf /tmp/*
  rm -rf /var/tmp/*
  rm -rf /usr/share/man
  rm -rf /usr/share/doc

  su - airflow >> EOF

    touch /home/airflow/.entrypoint_check

    if [ "$DB_TYPE" = "mysql" ]
    then
        sed -i -e 's/<mysql_db_connection>/sql_alchemy_conn = mysql:\/\/'$DB_USER':'$DB_PWD'@'$DB_HOST':'$DB_PORT'\/'$DB_NAME'/g' /home/airflow/airflow.cfg
    else
        sed -i -e 's/<mysql_db_connection>/sql_alchemy_conn = postgresql+psycopg2:\/\/'$DB_USER':'$DB_PWD'@'$DB_HOST':'$DB_PORT'\/'$DB_NAME'/g' /home/airflow/airflow.cfg
    fi

    if [ "$USE_WEX" = "yes" ]
    then
        echo "Setup WEX Server Key"
        cd /home/airflow
        mkdir .ssh
        ssh-keygen -f /home/airflow/.ssh/id_rsa -t rsa -N ''
        ssh -o "StrictHostKeyChecking no" -o PasswordAuthentication=no $WEX_USER@$WEX_HOST -p$WEX_PORT
        cat .ssh/id_rsa.pub | sshpass -p $WEX_PWD ssh $WEX_USER@$WEX_HOST -p$WEX_PORT 'cat >> .ssh/authorized_keys'
    fi

    echo "Setup done!"

    if [ "$IS_WEB" = "yes" ]
    then
      airflow initdb

      sleep 5
      python /home/airflow/set_auth.py

      airflow webserver
    else
      airflow scheduler
    fi
  EOF

fi
