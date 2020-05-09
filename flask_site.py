from flask import Flask, Blueprint, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from flask_api import Customer

site = Blueprint("site", __name__)

# Client webpage.
@site.route("/")
@login_required
def index():
    return render_template("index.html")

@site.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(Customer.query.filter_by(username=form.username.data).first(), remember=form.remember_me.data)
        return redirect(request.args.get('next') or "/")
    return render_template("login.html", form=form)

@site.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@site.route("/register", methods=["GET", "POST"])
def register():
    # Use REST API.
    form = RegisterForm()
    if form.validate_on_submit():
        requests.post("http://127.0.0.1:5000/api/customer", request.form)
        return redirect("/")
    return render_template("register.html", form=form)
