from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
from passlib.hash import sha256_crypt

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    username = db.Column(db.Text, unique = True)
    password = db.Column(db.Text)
    email = db.Column(db.Text)

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
    car_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    status = db.Column(db.Text)
    make = db.Column(db.Text)
    model = db.Column(db.Text)
    body_type = db.Column(db.Text)
    colour = db.Column(db.Text)
    seats = db.Column(db.Integer)
    location = db.Column(db.Text)
    cost_per_hour = db.Column(db.Float)

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
    car_id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, primary_key = True)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    status = db.Column(db.Text)

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
@api.route("/customers", methods = ["GET"])
def getCustomers():
    customers = Customer.query.all()
    result = customersSchema.dump(customers)

    return jsonify(result)

# Endpoint to get customer by id.
@api.route("/customer/<id>", methods = ["GET"])
def getCustomer(id):
    customer = Customer.query.get(id)
    return customerSchema.jsonify(customer)

# Endpoint to create new customer.
@api.route("/customer", methods = ["POST"])
def addCustomer():
    newCustomer = Customer(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        username=request.form["username"],
        password=sha256_crypt.using(rounds = 1000).hash(request.form["password"]),
        email=request.form["email"])
    db.session.add(newCustomer)
    db.session.commit()

    return customerSchema.jsonify(newCustomer)

# Endpoint to update person.
@api.route("/person/<id>", methods = ["PUT"])
def personUpdate(id):
    person = Person.query.get(id)
    name = json.loads(request.json)["name"]

    person.Name = name

    db.session.commit()

    return personSchema.jsonify(person)

# Endpoint to delete person.
@api.route("/person/<id>", methods = ["DELETE"])
def personDelete(id):
    person = Person.query.get(id)

    db.session.delete(person)
    db.session.commit()

    return personSchema.jsonify(person)
