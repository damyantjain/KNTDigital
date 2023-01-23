from flask import Flask
from kntdigital.config import Config
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

mysql = MySQL()
mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mysql.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    from kntdigital.main.routes import main
    from kntdigital.action.routes import action
    from kntdigital.action.employee.routes import employee

    app.register_blueprint(main)
    app.register_blueprint(action)
    app.register_blueprint(employee)
    return app
