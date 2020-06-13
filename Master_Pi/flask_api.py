from flask import Flask, Blueprint, request, jsonify, render_template
import os, requests, json
from flask import current_app as app
from passlib.hash import sha256_crypt
from flask_database import *
from calendar_utils import create_event, delete_event
from datetime import datetime

api = Blueprint("api", __name__)

def checkFieldsExist(form, *args):
    missing = []
    for arg in args:
        if arg not in form:
            missing.append(arg)
    if missing:
        message = ""
        for field in missing:
            message = message + field + ", "
        raise NameError("Form missing values for {}".format(message))

# Endpoint to show all customers.
@api.route("/api/customers", methods = ["GET"])
def getCustomers():
    """Endpoint to display all customers
    """
    customers = User.query.filter_by(user_type="customer").all()
    result = usersSchema.dump(customers)

    return jsonify(result)

# Endpoint to get customer by id.
@api.route("/api/customer/<int:customer_id>", methods = ["GET"])
def getCustomer(customer_id):
    """Endpoint to get customer by id
    """
    customer = User.query.get(customer_id)
    return userSchema.jsonify(customer)

# Endpoint to get customer by username.
@api.route("/api/customer/username/<username>", methods = ["GET"])
def getCustomerByUsername(username):
    """Endpoint to get customer by username
    """
    customer = User.query.filter_by(username=username, user_type="customer").first()
    return userSchema.jsonify(customer)

# Endpoint to get user by email.
@api.route("/api/user/email/<email>", methods = ["GET"])
def getCustomerByEmail(email):
    """Endpoint to get user by email
    """
    user = User.query.filter_by(email=email).first()
    return userSchema.jsonify(user)

# Endpoint to create new customer.
@api.route("/api/customer", methods = ["POST"])
def addCustomer():
    """Endpoint to create new customer
    """
    form = request.form
    checkFieldsExist(form, "first_name", "last_name", "username", "password", "email")
    newCustomer = User(
        first_name=form["first_name"],
        last_name=form["last_name"],
        username=form["username"],
        password=sha256_crypt.using(rounds = 1000).hash(form["password"]),
        email=form["email"],
        user_type="customer")
    db.session.add(newCustomer)
    db.session.commit()

    return userSchema.jsonify(newCustomer)

# Endpoint to verify username and password
@api.route("/api/user/verify", methods = ["POST"])
def verifyUser():
    """Endpoint to verify username and password
    """
    form = request.form
    checkFieldsExist(form, "username", "password")
    user = User.query.filter_by(username=form["username"]).first()
    if user:
        if sha256_crypt.verify(form["password"], user.password):
            return userSchema.jsonify(user)
    return userSchema.jsonify(None)

# Endpoint to get all cars
@api.route("/api/cars", methods = ["GET"])
def getCars():
    """Endpoint to get all cars
    """
    cars = Car.query.all()
    result = carsSchema.dump(cars)

    return jsonify(result)

# Endpoint to get car by id.
@api.route("/api/car/<int:car_id>", methods = ["GET"])
def getCar(car_id):
    """Endpoint to get a car by id
    """
    car = Car.query.get(car_id)
    return carSchema.jsonify(car)

# Endpoint to get cars by status
@api.route("/api/cars/status/<status>", methods = ["GET"])
def getCarsByStatus(status):
    """Endpoint to get a car by status
    """
    cars = Car.query.filter_by(status=status).all()
    result = carsSchema.dump(cars)

    return jsonify(result)

# method which returns cars with a status and certain property
def getCarsByStatusAndProperty(status, search_property, value):
    cars = db.engine.execute('SELECT * FROM car WHERE status = "{}" AND LOWER({}) LIKE LOWER("%%{}%%")'.format(status, search_property, value))
    result = carsSchema.dump(cars)

    return jsonify(result)

# method which returns cars with a certain property
def getCarsByProperty(search_property, value):
    cars = db.engine.execute('SELECT * FROM car WHERE LOWER({}) LIKE LOWER("%%{}%%")'.format(search_property, value))
    result = carsSchema.dump(cars)

    return jsonify(result)

# Endpoint to get available cars with a property
@api.route("/api/cars/available/property", methods = ["POST"])
def getCarsAvailableByProperty():
    form = request.form
    checkFieldsExist(form, "search_property", "search")
    return getCarsByStatusAndProperty("available", form["search_property"], form["search"])

# Endpoint to get cars with a property
@api.route("/api/cars/property", methods = ["POST"])
def getAllCarsByProperty():
    form = request.form
    checkFieldsExist(form, "search_property", "search")
    return getCarsByProperty(form["search_property"], form["search"])

# Endpoint to get all bookings
@api.route("/api/bookings", methods = ["GET"])
def getBookings():
    """Endpoint to get all bookings
    """
    bookings = Booking.query.all()
    result = bookingsSchema.dump(bookings)

    return jsonify(result)

# Endpoint to get bookings by customer
@api.route("/api/bookings/<int:customer_id>", methods = ["GET"])
def getBookingsByCustomer(customer_id):
    """Endpoint to get booking by customer
    """
    bookings = Booking.query.filter_by(user_id=customer_id).all()
    result = bookingsSchema.dump(bookings)

    return jsonify(result)

def getBookingsByCustomerAndStatus(customer_id, status):
    """Endpoint to get bookings by customer and status
    """
    bookings = Booking.query.filter_by(user_id=customer_id, status=status).all()
    result = bookingsSchema.dump(bookings)

    return jsonify(result)

# Endpoint to get a customer's active bookings
@api.route("/api/bookings/customer/<int:customer_id>/status/active", methods = ["GET"])
def getCustomersActiveBookings(customer_id):
    """Endpoint to get a customer's active bookings
    """
    return getBookingsByCustomerAndStatus(customer_id, "active")

# Endpoint to get a car's active booking
@api.route("/api/booking/car/<int:car_id>/status/active", methods = ["GET"])
def getCarsActiveBooking(car_id):
    booking = Booking.query.filter_by(car_id=car_id, status="active").first()
    result = bookingSchema.dump(booking)

    return jsonify(result)

# Endpoint to get a customer's complete bookings
@api.route("/api/bookings/customer/<int:customer_id>/status/complete", methods = ["GET"])
def getCustomersCompleteBookings(customer_id):
    """Endpoint to get a customer's complete bookings
    """
    return getBookingsByCustomerAndStatus(customer_id, "complete")

# Endpoint to get a customer's cancelled bookings
@api.route("/api/bookings/customer/<int:customer_id>/status/cancelled", methods = ["GET"])
def getCustomersCancelledBookings(customer_id):
    """Endpoint to get a customer's cancelled bookings
    """
    return getBookingsByCustomerAndStatus(customer_id, "cancelled")

# Endpoint to book a car
@api.route("/api/booking", methods = ["POST"])
def addBooking():
    """Endpoint to book a car
    """
    form = request.form
    checkFieldsExist(form, "car_id", "customer_id", "start_datetime", "end_datetime")

    car = Car.query.get(form["car_id"])
    customer = User.query.get(form["customer_id"])
    description = "car details - Make: {}, Model: {}, Body Type: {}, Colour: {}, Seats: {}, Location: {}, Cost Per Hour: ${}\nBooked by {}".format(
        car.make, car.model, car.body_type, car.colour, car.seats, car.location, car.cost_per_hour, customer.username)
    event = create_event(
        form["start_datetime"]+":00", form["end_datetime"]+":00", "Booking for car {} {}".format(car.make, car.model), 
        description=description)
    if event != None:
        event_id = event['id']
    else:
        event_id = None

    newBooking = Booking(
        car_id=form["car_id"],
        user_id=form["customer_id"],
        start_datetime=form["start_datetime"],
        end_datetime=form["end_datetime"],
        status="active",
        calendar_id=event_id)
    
    car.status = "unavailable"

    db.session.add(newBooking)
    db.session.commit()

    return bookingSchema.jsonify(newBooking)

def setBookingStatus(car_id, customer_id, start_datetime, status):
    """Endpoint to set the status of a booking
    """
    booking = Booking.query.filter_by(
        car_id=car_id, 
        user_id=customer_id,
        start_datetime=start_datetime).first()
    if booking:
        booking.status = status

        car = Car.query.get(car_id)
        if status != "active":
            car.status = "available"
            if status == "cancelled":
                delete_event(booking.calendar_id)
        else:
            car.status = "unavailable"

        db.session.commit()

        return bookingSchema.jsonify(booking)
    return bookingSchema.jsonify(None)

# Endpoint to update booking status to cancelled
@api.route("/api/booking/status/cancelled", methods = ["PUT"])
def setBookingStatusCancelled():
    """Endpoint to update booking status to cancelled
    """
    form = request.form
    checkFieldsExist(form, "car_id", "customer_id", "start_datetime")
    return setBookingStatus(form["car_id"], form["customer_id"], form["start_datetime"], "cancelled")

# Endpoint to update booking status to complete
@api.route("/api/booking/status/complete", methods = ["PUT"])
def setBookingStatusComplete():
    """Endpoint to update booking status to complete
    """
    form = request.form
    checkFieldsExist(form, "car_id", "customer_id", "start_datetime")
    return setBookingStatus(form["car_id"], form["customer_id"], form["start_datetime"], "complete")

# Endpoint to get user by username.
@api.route("/api/user/username/<username>", methods = ["GET"])
def getUserByUsername(username):
    """Endpoint to get user by username
    """
    user = User.query.filter_by(username=username).first()
    return userSchema.jsonify(user)

@api.route("/api/engineer/<int:engineer_id>/issues", methods = ["GET"])
def getEngineersIssues(engineer_id):
    issues = Issue.query.filter_by(engineer_id=engineer_id).all()
    result = issuesSchema.dump(issues)

    return issuesSchema.jsonify(result)

@api.route("/api/engineer/<int:engineer_id>/issues/resolved", methods = ["GET"])
def getEngineersResolvedIssues(engineer_id):
    issues = Issue.query.filter_by(engineer_id=engineer_id, status="resolved").all()
    result = issuesSchema.dump(issues)

    return issuesSchema.jsonify(result)

@api.route("/api/engineer/<int:engineer_id>/issues/unresolved", methods = ["GET"])
def getEngineersUnresolvedIssues(engineer_id):
    issues = Issue.query.filter_by(engineer_id=engineer_id, status="unresolved").all()
    result = issuesSchema.dump(issues)

    return issuesSchema.jsonify(result)


@api.route("/api/bookings/car/<int:car_id>", methods = ["GET"])
def getCarsBookings(car_id):
    bookings = Booking.query.filter_by(car_id=car_id)
    result = bookingsSchema.dump(bookings)

    return bookingsSchema.jsonify(result)

@api.route("/api/users", methods=["GET"])
def getUsers():
    users = User.query.all()
    result = usersSchema.dump(users)

    return usersSchema.jsonify(result)

@api.route("/api/engineers", methods = ["GET"])
def getEngineers():
    engineers = User.query.filter_by(user_type="engineer").all()
    result = usersSchema.dump(engineers)

    return usersSchema.jsonify(result)

@api.route("/api/user/<int:user_id>", methods = ["GET"])
def getUser(user_id):
    """Endpoint to get user by id
    """
    user = User.query.get(user_id)
    return userSchema.jsonify(user)

@api.route("/api/user", methods=["PUT"])
def updateUser():
    form = request.form
    checkFieldsExist(form, "user_id", "first_name", "last_name", "username", "email", "user_type")
    user = User.query.get(form["user_id"])
    user.first_name = form["first_name"]
    user.last_name = form["last_name"]
    user.username = form["username"]
    user.email = form["email"]
    user.user_type = form["user_type"]
    db.session.commit()
    return userSchema.jsonify(user)

@api.route("/api/car", methods=["PUT"])
def updateCar():
    form = request.form
    checkFieldsExist(form, "car_id", "status", "make", "model", "body_type", "colour", "seats", "cost_per_hour")
    car = Car.query.get(form["car_id"])
    car.status = form["status"]
    car.make = form["make"]
    car.model = form["model"]
    car.body_type = form["body_type"]
    car.colour = form["colour"]
    car.seats = form["seats"]
    car.cost_per_hour = form["cost_per_hour"]
    if form["status"] == "unavailable":
        activeBooking = Booking.query.filter_by(car_id=form["car_id"], status="active").first()
        if activeBooking:
            activeBooking.status = "cancelled"
    db.session.commit()
    return carSchema.jsonify(car)

@api.route("/api/car/<int:car_id>/history")
def getCarHistory(car_id):
    bookings = Booking.query.filter_by(car_id=car_id).all()
    result = bookingsSchema.dump(bookings)

    return jsonify(result)

@api.route("/api/issue", methods=["POST"])
def createIssue():
    form = request.form
    checkFieldsExist(form, "description", "status", "engineer_id", "car_id")
    newIssue = Issue(
        description=form["description"],
        date_reported=datetime.now(),
        status=form["status"],
        engineer_id=form["engineer_id"],
        car_id=form["car_id"])

    Car.query.get(form["car_id"]).status = "unavailable"
    activeBooking = Booking.query.filter_by(car_id=form["car_id"], status="active").first()
    if activeBooking:
        activeBooking.status = "cancelled"
    db.session.add(newIssue)
    db.session.commit()

    return issueSchema.jsonify(newIssue)

@api.route("/api/users/property", methods =["POST"])
def getUsersByProperty():
    form = request.form
    checkFieldsExist(form, "search_property", "search")
    users = db.engine.execute('SELECT * FROM user WHERE LOWER({}) LIKE LOWER("%%{}%%")'.format(form["search_property"], form["search"]))
    result = usersSchema.dump(users)

    return usersSchema.jsonify(result)