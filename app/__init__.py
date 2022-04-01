from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Войдите, чтобы получить доступ к странице'
bootstrap = Bootstrap(app)

from app import routes, models