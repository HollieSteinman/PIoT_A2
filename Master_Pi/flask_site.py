from flask import Flask, Blueprint, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from forms import LoginForm, RegisterForm, SearchForm
from flask_login import login_user, logout_user, login_required, current_user
from flask_database import Customer

site = Blueprint("site", __name__)

# Client webpage.
@site.route("/")
@login_required
def index():
    return render_template("index.html")

@site.route("/login", methods=["GET", "POST"])
def login():
    """Serve customer login page
    """
    if current_user.is_authenticated:
        return redirect("/")
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
    """Serve customer registration page
    """
    if current_user.is_authenticated:
        logout()
    form = RegisterForm()
    if form.validate_on_submit():
        requests.post("http://127.0.0.1:5000/api/customer", data=request.form)
        return redirect("/login")
    return render_template("register.html", form=form)

@site.route("/cars", methods=["GET", "POST"])
@login_required
def cars():
    """Serve car listing page
    """
    form = SearchForm()
    if request.method == "POST" and "car_id" in request.form:
        return redirect("/booking/" + request.form["car_id"])
    if form.is_submitted():
        response = requests.post("http://127.0.0.1:5000/api/cars/available/property", data=request.form)
    else:
        response = requests.get("http://127.0.0.1:5000/api/cars/status/available")
    data = json.loads(response.text)
    return render_template("cars.html", available_cars=data, form=form)

@site.route("/booking/<int:car_id>", methods=["GET", "POST"])
@login_required
def booking(car_id):
    """Serve view booking page by car id
    """
    response = requests.get("http://127.0.0.1:5000/api/car/{}".format(car_id))
    data = json.loads(response.text)
    if data["status"] == "available":
        if request.method == "POST":
            requests.post("http://127.0.0.1:5000/api/booking", data=request.form)
            return redirect("/bookings")
        else:
            return render_template("booking.html", car = data)
    else:
        return redirect("/cars")

@site.route("/bookings", methods=["GET", "POST"])
@login_required
def bookings():
    """Serve booking listing page by id
    """
    if request.method == "POST":
        requests.put("http://127.0.0.1:5000/api/booking/status/cancelled", data=request.form)
    activeBookings = json.loads(requests.get("http://127.0.0.1:5000/api/bookings/customer/{}/status/active".format(current_user.customer_id)).text)
    completeBookings = json.loads(requests.get("http://127.0.0.1:5000/api/bookings/customer/{}/status/complete".format(current_user.customer_id)).text)
    cancelledBookings = json.loads(requests.get("http://127.0.0.1:5000/api/bookings/customer/{}/status/cancelled".format(current_user.customer_id)).text)

    return render_template("bookings.html", activeBookings = activeBookings, completeBookings = completeBookings, cancelledBookings = cancelledBookings)
