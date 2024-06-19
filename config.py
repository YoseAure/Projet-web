import os
from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'enac.darties.fr')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'aurelien.collet')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'u27dPvXHAzeUPzp4')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'les_apprentis')

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
