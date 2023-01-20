from flask import Flask
from kntdigital.config import Config
from flask_mysqldb import MySQL

mysql = MySQL()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mysql.init_app(app)

    from kntdigital.main.routes import main

    app.register_blueprint(main)
    return app
