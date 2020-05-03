from wtforms.validators import ValidationError
import requests, json

def unique_username(form, field):
    # check if username does not exist in database
    customers = requests.get("http://127.0.0.1:5000/customers").json()
    for customer in customers:
        if customer["username"] == field.data:
            raise ValidationError("Username already taken")

def username_exists(form, field):
    # check if username exists in database
    # customers = requests.get("http://127.0.0.1:5000/customers")
    pass

# have method to check if password matches given username
