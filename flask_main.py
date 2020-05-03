# pip3 install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy
# python3 flask_main.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask_api import api, db
from flask_site import site
from flask_bootstrap import Bootstrap
from config import Config

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

app.register_blueprint(api)
app.register_blueprint(site)
app.config.from_object(Config)

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
