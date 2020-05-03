from flask import Flask, Blueprint, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from forms import LoginForm, RegisterForm

site = Blueprint("site", __name__)

# Client webpage.
@site.route("/")
def index():
    return render_template("index.html", data={"name":"Moose"})

@site.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Username: {}, Password: {}".format(form.username.data, form.password.data))
        return redirect("/")
    return render_template("login.html", form=form)

@site.route("/register", methods=["GET", "POST"])
def register():
    # Use REST API.
    form = RegisterForm()
    if form.validate_on_submit():
        requests.post("http://127.0.0.1:5000/customer", request.form)
        # print("First Name: {}, Last Name: {}, Username: {}, Password: {}, Email: {}".format(form.first_name.data, 
        #     form.last_name.data, form.username.data, form.password.data, form.email.data))
        return redirect("/")
    return render_template("register.html", form=form)
