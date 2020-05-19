# pip3 install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy
# python3 flask_main.py
from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask_api import api
from flask_database import db, Customer
from flask_site import site
from flask_bootstrap import Bootstrap
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
bs = Bootstrap(app)

# Update HOST and PASSWORD appropriately.
HOST = "35.197.185.32"
USER = "root"
PASSWORD = "3645"
DATABASE = "car_share"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

@login_manager.user_loader
def load_user(user_id):
    """Load the current user using the login manager
    """
    return Customer.query.get(user_id)

app.register_blueprint(api)
app.register_blueprint(site)
app.config.from_object(Config)

if __name__ == "__main__":
    """Run the flask application on localhost
    """
    app.run(host = "0.0.0.0")
