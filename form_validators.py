from wtforms.validators import ValidationError
import requests, json

def unique_username(form, field):
    # check if username does not exist in database
    customer = requests.get("http://127.0.0.1:5000/customer/username/" + field.data).json()
    if customer:
        raise ValidationError("Username already taken")

def username_exists(form, field):
    # check if username exists in database
    # customers = requests.get("http://127.0.0.1:5000/customers")
    pass

# have method to check if password matches given username
