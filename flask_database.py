from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import UserMixin

db = SQLAlchemy()
ma = Marshmallow()

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
