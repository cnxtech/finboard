from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
from airflow.models import Variable
from flask_bcrypt import generate_password_hash

# Get password from variables
password = Variable.get("user_password")

user = PasswordUser(models.User())
user.username = 'admin'
user.email = 'swalloow.me@gmail.com'
user._password = generate_password_hash(password, 12)

session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()
