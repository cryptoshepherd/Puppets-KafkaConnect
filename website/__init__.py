from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    with open('config.json') as config_file:
        config = json.load(config_file)
    app.config['SECRET_KEY'] = config.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    # Views
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # SQLAlchemy
    create_database(app)

    return app


# SQLAlchemy DB Creation
def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")

