from flask import Flask, Blueprint, request, jsonify, render_template
import os, requests, json
from flask import current_app as app
from passlib.hash import sha256_crypt
from flask_database import *
from calendar_utils import create_event, delete_event

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

# Endpoint to get customer by email.
@api.route("/api/customer/email/<email>", methods = ["GET"])
def getCustomerByEmail(email):
    """Endpoint to get customer by email
    """
    customer = User.query.filter_by(email=email, user_type="customer").first()
    return userSchema.jsonify(customer)

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
@api.route("/api/customer/verify", methods = ["POST"])
def verifyCustomer():
    """Endpoint to verify username and password
    """
    form = request.form
    checkFieldsExist(form, "username", "password")
    customer = User.query.filter_by(username=form["username"], user_type="customer").first()
    if customer:
        if sha256_crypt.verify(form["password"], customer.password):
            return userSchema.jsonify(customer)
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

# Endpoint to get available cars with a property
@api.route("/api/cars/available/property", methods = ["POST"])
def getCarsAvailableByProperty():
    form = request.form
    return getCarsByStatusAndProperty("available", form["search_property"], form["search"])

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
