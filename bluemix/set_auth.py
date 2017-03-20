import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'username'
user.email = 'your@email.com'
user.password = 'pwd'
session = settings.Session()
session.add(user)
session.commit()
session.close()
