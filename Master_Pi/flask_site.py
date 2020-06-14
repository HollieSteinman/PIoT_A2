from flask import Flask, Blueprint, request, jsonify, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from forms import LoginForm, RegisterForm, CarsSearchForm, EditUserForm, EditCarForm, ReportIssueForm, UsersSearchForm, AllCarsSearchForm
from flask_login import login_user, logout_user, login_required, current_user
from flask_database import User

site = Blueprint("site", __name__)

def cars_as_dict():
    cars = requests.get("http://127.0.0.1:5000/api/cars").json()
    cars_dict = {}
    for car in cars:
        cars_dict[car["car_id"]] = car
    return cars_dict

def users_as_dict():
    users = requests.get("http://127.0.0.1:5000/api/users").json()
    users_dict = {}
    for user in users:
        users_dict[user["user_id"]] = user
    return users_dict

@site.route("/login", methods=["GET", "POST"])
def login():
    """Serve customer login page
    """
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        login_user(User.query.filter_by(username=form.username.data).first(), remember=form.remember_me.data)
        return redirect(request.args.get('next') or "/")
    return render_template("login.html", form=form)

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

@site.route("/unauthorised", methods = ["GET"])
def unauthorised():
    return render_template("unauthorised.html")

@site.route("/")
@login_required
def index():
    return render_template("index.html")

@site.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# Customer Pages
@site.route("/cars", methods=["GET", "POST"])
@login_required
def cars():
    """Serve car listing page
    """
    if (current_user.user_type != "customer"):
        return redirect("/unauthorised")

    form = CarsSearchForm()
    if form.validate_on_submit():
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
    if (current_user.user_type != "customer"):
        return redirect("/unauthorised")

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
    if (current_user.user_type != "customer"):
        return redirect("/unauthorised")

    if request.method == "POST":
        requests.put("http://127.0.0.1:5000/api/booking/status/cancelled", data=request.form)
    activeBookings = json.loads(requests.get("http://127.0.0.1:5000/api/bookings/customer/{}/status/active".format(current_user.user_id)).text)
    completeBookings = json.loads(requests.get("http://127.0.0.1:5000/api/bookings/customer/{}/status/complete".format(current_user.user_id)).text)
    cancelledBookings = json.loads(requests.get("http://127.0.0.1:5000/api/bookings/customer/{}/status/cancelled".format(current_user.user_id)).text)

    return render_template("bookings.html", activeBookings = activeBookings, 
    completeBookings = completeBookings, cancelledBookings = cancelledBookings, cars=cars_as_dict())

# End of Customer Pages

# Admin Pages
@site.route("/users", methods = ["GET", "POST"])
@login_required
def users():
    if (current_user.user_type != "admin"):
        return redirect("/unauthorised")

    form = UsersSearchForm()
    if form.validate_on_submit():
        users = requests.post("http://127.0.0.1:5000/api/users/property", data=request.form).json()
    else:
        users = requests.get("http://127.0.0.1:5000/api/users").json()
    return render_template("users.html", form=form, users=users)

@site.route("/edit/user/<int:user_id>", methods = ["GET", "POST"])
@login_required
def editUser(user_id):
    if (current_user.user_type != "admin"):
        return redirect("/unauthorised")

    form = EditUserForm()
    if form.validate_on_submit():
        requests.put("http://127.0.0.1:5000/api/user", data=request.form)
        flash("User details updated successfully", "details_updated")
    user = requests.get("http://127.0.0.1:5000/api/user/{}".format(user_id)).json()
    if not form.is_submitted():
        form.fill_data(user)
    return render_template("edit_user.html", form = form, user = user)

@site.route("/cars/all", methods = ["GET", "POST"])
@login_required
def allCars():
    if (current_user.user_type != "admin"):
        return redirect("/unauthorised")

    form = AllCarsSearchForm()
    if form.validate_on_submit():
        response = requests.post("http://127.0.0.1:5000/api/cars/property", data=request.form)
    else:
        response = requests.get("http://127.0.0.1:5000/api/cars")
    data = json.loads(response.text)
    return render_template("all_cars.html", form=form, cars=data)

@site.route("/edit/car/<int:car_id>", methods = ["GET", "POST"])
@login_required
def editCar(car_id):
    if (current_user.user_type != "admin"):
        return redirect("/unauthorised")

    form = EditCarForm()
    if form.validate_on_submit():
        requests.put("http://127.0.0.1:5000/api/car", data=request.form)
        flash("Car details updated successfully", "details_updated")
    car = requests.get("http://127.0.0.1:5000/api/car/{}".format(car_id)).json()
    if not form.is_submitted():
        form.fill_data(car)
    return render_template("edit_car.html", form=form, car=car)

@site.route("/car/<int:car_id>/history", methods=["GET"])
@login_required
def carHistory(car_id):
    if (current_user.user_type != "admin"):
        return redirect("/unauthorised")

    car = requests.get("http://127.0.0.1:5000/api/car/{}".format(car_id)).json()
    bookings = requests.get("http://127.0.0.1:5000/api/car/{}/history".format(car_id)).json()
    return render_template("rental_history.html", car=car, bookings=bookings, users=users_as_dict())

def format_new_issue_body(car_id, form):
    issue_body = "Issue Details\n"
    car = requests.get("http://127.0.0.1:5000/api/car/{}".format(car_id)).json()
    issue_body += "car: " + car["make"] + " " + car["model"] + "\n"
    issue_body += "description: " + form["description"] + "\n"
    issue_body += "status: " + form["status"]
    return issue_body

@site.route("/car/<int:car_id>/issue", methods=["GET", "POST"])
@login_required
def reportIssue(car_id):
    if (current_user.user_type != "admin"):
        return redirect("/unauthorised")

    form = ReportIssueForm()
    if form.validate_on_submit():
        # update car and add a new issue to the table (api)
        requests.post("http://127.0.0.1:5000/api/issue", data=request.form)
        send_notification_via_pushbullet("New Issue Assigned", format_new_issue_body(car_id, request.form))
        return redirect("/cars/all")
    form.fill_data(car_id, requests.get("http://127.0.0.1:5000/api/engineers").json())
    car = requests.get("http://127.0.0.1:5000/api/car/{}".format(car_id)).json()
    return render_template("issue.html", form=form, car=car)
# End of Admin Pages

# Engineer Pages
@site.route("/issues", methods=["GET"])
@login_required
def issues():
    if (current_user.user_type != "engineer"):
        return redirect("/unauthorised")

    unresolved_issues = requests.get("http://127.0.0.1:5000/api/engineer/{}/issues/unresolved".format(current_user.user_id)).json()
    resolved_issues = requests.get("http://127.0.0.1:5000/api/engineer/{}/issues/resolved".format(current_user.user_id)).json()
    return render_template("issues.html", cars=cars_as_dict(), unresolved_issues=unresolved_issues, resolved_issues=resolved_issues)
# End of Engineer Pages

# Manager Pages
@site.route("/data", methods=["GET"])
@login_required
def dataAnalytics():
    if (current_user.user_type != "manager"):
        return redirect("/unauthorised")

    return render_template("data_analytics.html")
# End of Manager Pages
