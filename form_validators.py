from wtforms.validators import ValidationError
import requests
from flask_api import Customer
from passlib.hash import sha256_crypt

def unique_username(form, field):
    # check if username does not exist in database
    customer = requests.get("http://127.0.0.1:5000/api/customer/username/" + field.data).json()
    if customer:
        raise ValidationError("Username already taken")

def login_details_correct(form, field):
    if form.username.data and form.password.data:
        message = "Username or Password incorrect" 
        user = Customer.query.filter_by(username=form.username.data).first()
        if not user:
            raise ValidationError(message)
        else:
            # if not sha256_crypt.verify(form.password.data, user.password):
            print(form.password.data)
            print(user.password)
            if not form.password.data == user.password:
                raise ValidationError(message)
