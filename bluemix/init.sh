if [ -e /home/airflow/.entrypoint_check ]
then
  if [ "$IS_WEB" = "yes" ]
  then
    echo "Starting Airflow Webserver"
    airflow initdb

    sleep 5

    airflow webserver
  else
    echo "Starting Airflow Scheduler"
    airflow scheduler
  fi

else
  touch /home/airflow/.entrypoint_check

  if [ "$DB_TYPE" = "mysql" ]
  then
      echo "MySQL db detected - changing airflow.cfg file"
      sed -i -e 's/<mysql_db_connection>/sql_alchemy_conn = mysql:\/\/'$DB_USER':'$DB_PWD'@'$DB_HOST':'$DB_PORT'\/'$DB_NAME'/g' /home/airflow/airflow.cfg
  else
      echo "Postgres db detected - changing airflow.cfg file"
      sed -i -e 's/<mysql_db_connection>/sql_alchemy_conn = postgresql+psycopg2:\/\/'$DB_USER':'$DB_PWD'@'$DB_HOST':'$DB_PORT'\/'$DB_NAME'/g' /home/airflow/airflow.cfg
  fi

  echo "Database setup done!"

  if [ "$USE_WEX" = "yes" ]
  then
      echo "Setup SSH to WEX Server"
      cd /home/airflow
      mkdir .ssh
      ssh-keygen -f /home/airflow/.ssh/id_rsa -t rsa -N ""
      ssh -o "StrictHostKeyChecking no" -o PasswordAuthentication=no $WEX_USER@$WEX_HOST -p$WEX_PORT
      cat .ssh/id_rsa.pub | sshpass -p $WEX_PWD ssh $WEX_USER@$WEX_HOST -p$WEX_PORT "cat >> .ssh/authorized_keys"
      echo "SSH Setup done!"
  fi

  echo "Setup done!"

  if [ "$IS_WEB" = "yes" ]
  then
    echo "Starting Airflow Webserver"
    airflow initdb

    sleep 5
    python /home/airflow/set_auth.py

    airflow webserver
  else
    echo "Starting Airflow Scheduler"
    airflow scheduler
  fi
fi
