from flask import Flask, Blueprint, request, jsonify, render_template
import os, requests, json
from flask import current_app as app
from passlib.hash import sha256_crypt
from flask_database import *
from calendar_utils import create_event

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
    customers = Customer.query.all()
    result = customersSchema.dump(customers)

    return jsonify(result)

# Endpoint to get customer by id.
@api.route("/api/customer/<int:customer_id>", methods = ["GET"])
def getCustomer(customer_id):
    customer = Customer.query.get(customer_id)
    return customerSchema.jsonify(customer)

# Endpoint to get customer by username.
@api.route("/api/customer/username/<username>", methods = ["GET"])
def getCustomerByUsername(username):
    customer = Customer.query.filter_by(username=username).first()
    return customerSchema.jsonify(customer)

# Endpoint to get customer by email.
@api.route("/api/customer/email/<email>", methods = ["GET"])
def getCustomerByEmail(email):
    customer = Customer.query.filter_by(email=email).first()
    return customerSchema.jsonify(customer)

# Endpoint to create new customer.
@api.route("/api/customer", methods = ["POST"])
def addCustomer():
    form = request.form
    checkFieldsExist(form, "first_name", "last_name", "username", "password", "email")
    newCustomer = Customer(
        first_name=form["first_name"],
        last_name=form["last_name"],
        username=form["username"],
        password=sha256_crypt.using(rounds = 1000).hash(form["password"]),
        email=form["email"])
    db.session.add(newCustomer)
    db.session.commit()

    return customerSchema.jsonify(newCustomer)

# Endpoint to verify username and password
@api.route("/api/customer/verify", methods = ["POST"])
def verifyCustomer():
    form = request.form
    checkFieldsExist(form, "username", "password")
    customer = Customer.query.filter_by(username=form["username"]).first()
    if customer:
        if sha256_crypt.verify(form["password"], customer.password):
            return customerSchema.jsonify(customer)
    return customerSchema.jsonify(None)

# Endpoint to get all cars
@api.route("/api/cars", methods = ["GET"])
def getCars():
    cars = Car.query.all()
    result = carsSchema.dump(cars)

    return jsonify(result)

# Endpoint to get car by id.
@api.route("/api/car/<int:car_id>", methods = ["GET"])
def getCar(car_id):
    car = Car.query.get(car_id)
    return carSchema.jsonify(car)

# Endpoint to get cars by status
@api.route("/api/cars/status/<status>", methods = ["GET"])
def getCarsByStatus(status):
    cars = Car.query.filter_by(status=status).all()
    result = carsSchema.dump(cars)

    return jsonify(result)

def getCarsByStatusAndProperty(status, search_property, value):
    cars = db.engine.execute('SELECT * FROM car WHERE status = "{}" AND LOWER({}) LIKE LOWER("%%{}%%")'.format(status, search_property, value))
    result = carsSchema.dump(cars)

    return jsonify(result)

@api.route("/api/cars/available/property", methods = ["POST"])
def getCarsAvailableByProperty():
    form = request.form
    return getCarsByStatusAndProperty("available", form["search_property"], form["search"])

# Endpoint to get all bookings
@api.route("/api/bookings", methods = ["GET"])
def getBookings():
    bookings = Booking.query.all()
    result = bookingsSchema.dump(bookings)

    return jsonify(result)

# Endpoint to get bookings by customer
@api.route("/api/bookings/<int:customer_id>", methods = ["GET"])
def getBookingsByCustomer(customer_id):
    bookings = Booking.query.filter_by(customer_id=customer_id).all()
    result = bookingsSchema.dump(bookings)

    return jsonify(result)

def getBookingsByCustomerAndStatus(customer_id, status):
    bookings = Booking.query.filter_by(customer_id=customer_id, status=status).all()
    result = bookingsSchema.dump(bookings)

    return jsonify(result)

# Endpoint to get a customer's active bookings
@api.route("/api/bookings/customer/<int:customer_id>/status/active", methods = ["GET"])
def getCustomersActiveBookings(customer_id):
    return getBookingsByCustomerAndStatus(customer_id, "active")

# Endpoint to get a customer's complete bookings
@api.route("/api/bookings/customer/<int:customer_id>/status/complete", methods = ["GET"])
def getCustomersCompleteBookings(customer_id):
    return getBookingsByCustomerAndStatus(customer_id, "complete")

# Endpoint to get a customer's cancelled bookings
@api.route("/api/bookings/customer/<int:customer_id>/status/cancelled", methods = ["GET"])
def getCustomersCancelledBookings(customer_id):
    return getBookingsByCustomerAndStatus(customer_id, "cancelled")

# Endpoint to book a car
@api.route("/api/booking", methods = ["POST"])
def addBooking():
    form = request.form
    checkFieldsExist(form, "car_id", "customer_id", "start_datetime", "end_datetime")

    car = Car.query.get(request.form["car_id"])
    event = create_event(form["start_datetime"]+":00", form["end_datetime"]+":00", "Booking for car {} {}".format(car.make, car.model))

    newBooking = Booking(
        car_id=form["car_id"],
        customer_id=form["customer_id"],
        start_datetime=form["start_datetime"],
        end_datetime=form["end_datetime"],
        status="active")
    
    car.status = "unavailable"

    db.session.add(newBooking)
    db.session.commit()

    return bookingSchema.jsonify(newBooking)

def setBookingStatus(car_id, customer_id, start_datetime, status):
    booking = Booking.query.filter_by(
        car_id=car_id, 
        customer_id=customer_id, 
        start_datetime=start_datetime).first()
    booking.status = status

    car = Car.query.get(car_id)
    if status != "active":
        car.status = "available"
    else:
        car.status = "unavailable"

    db.session.commit()

    return bookingSchema.jsonify(booking)

# Endpoint to update booking status to cancelled
@api.route("/api/booking/status/cancelled", methods = ["PUT"])
def setBookingStatusCancelled():
    form = request.form
    checkFieldsExist(form, "car_id", "customer_id", "start_datetime")
    return setBookingStatus(form["car_id"], form["customer_id"], form["start_datetime"], "cancelled")

# Endpoint to update booking status to complete
@api.route("/api/booking/status/complete", methods = ["PUT"])
def setBookingStatusComplete():
    form = request.form
    checkFieldsExist(form, "car_id", "customer_id", "start_datetime")
    return setBookingStatus(form["car_id"], form["customer_id"], form["start_datetime"], "complete")
