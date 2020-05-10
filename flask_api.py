from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
from passlib.hash import sha256_crypt
from flask_login import UserMixin

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

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

# Declaring the model.
class Customer(UserMixin, db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, unique = True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique = True, nullable=False)

    def get_id(self):
        return self.customer_id

    def __init__(self, first_name, last_name, username, password, email, customer_id=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email

class CustomerSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(**kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("customer_id", "first_name", "last_name", "username", "email")

customerSchema = CustomerSchema()
customersSchema = CustomerSchema(many = True)

class Car(db.Model):
    __tablename__ = "car"
    car_id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True, nullable=False)
    status = db.Column(db.Text, nullable=False)
    make = db.Column(db.Text, nullable=False)
    model = db.Column(db.Text, nullable=False)
    body_type = db.Column(db.Text, nullable=False)
    colour = db.Column(db.Text, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    location = db.Column(db.Text, nullable=False)
    cost_per_hour = db.Column(db.Float, nullable=False)

    def __init__(self, status, make, model, body_type, colour, seats, location, cost_per_hour, car_id=None):
        self.car_id = car_id
        self.status = status
        self.make = make
        self.model = model
        self.body_type = body_type
        self.colour = colour
        self.seats = seats
        self.location = location
        self.cost_per_hour = cost_per_hour

class CarSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(**kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("car_id", "status", "make", "model", "body_type", "colour", "seats", "location", "cost_per_hour")

carSchema = CarSchema()
carsSchema = CarSchema(many = True)

class Booking(db.Model):
    __tablename__ = "booking"
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'), primary_key = True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key = True, nullable=False)
    start_datetime = db.Column(db.DateTime, primary_key = True, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Text, nullable=False)

    def __init__(self, car_id, customer_id, start_datetime, end_datetime, status):
        self.car_id = car_id
        self.customer_id = customer_id
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.status = status

class BookingSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(**kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("car_id", "customer_id", "start_datetime", "end_datetime", "status")

bookingSchema = BookingSchema()
bookingsSchema = BookingSchema(many = True)

# Endpoint to show all customers.
@api.route("/api/customers", methods = ["GET"])
def getCustomers():
    customers = Customer.query.all()
    result = customersSchema.dump(customers)

    return jsonify(result)

# Endpoint to get customer by id.
@api.route("/api/customer/<int:id>", methods = ["GET"])
def getCustomer(id):
    customer = Customer.query.get(id)
    return customerSchema.jsonify(customer)

# Endpoint to get customer by username.
@api.route("/api/customer/username/<username>", methods = ["GET"])
def getCustomerByUsername(username):
    customer = Customer.query.filter_by(username=username).first()
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

# Endpoint to get all cars
@api.route("/api/cars", methods = ["GET"])
def getCars():
    cars = Car.query.all()
    result = carsSchema.dump(cars)

    return jsonify(result)

# Endpoint to get car by id.
@api.route("/api/car/<int:id>", methods = ["GET"])
def getCar(id):
    car = Car.query.get(id)
    return carSchema.jsonify(car)

# Endpoint to get cars by status
@api.route("/api/cars/status/<status>", methods = ["GET"])
def getCarsByStatus(status):
    cars = Car.query.filter_by(status=status).all()
    result = carsSchema.dump(cars)

    return jsonify(result)

# Endpoint to get all bookings
@api.route("/api/bookings", methods = ["GET"])
def getBookings(customer_id):
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
    newBooking = Booking(
        car_id=form["car_id"],
        customer_id=form["customer_id"],
        start_datetime=form["start_datetime"],
        end_datetime=form["end_datetime"],
        status="active")
    
    car = Car.query.get(request.form["car_id"])
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
