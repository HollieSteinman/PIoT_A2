from wtforms.validators import ValidationError
import requests

def unique_username(form, field):
    # check if username does not exist in database
    customer = requests.get("http://127.0.0.1:5000/api/customer/username/" + field.data).json()
    if customer:
        raise ValidationError("Username already taken")

def unique_email(form, field):
    customer = requests.get("http://127.0.0.1:5000/api/customer/email/" + field.data).json()
    if customer:
        raise ValidationError("Eamil used by another account")

def login_details_correct(form, field):
    if form.username.data and form.password.data:
        data = {"username":form.username.data, "password":form.password.data}
        if not requests.post("http://127.0.0.1:5000/api/customer/verify", data=data).json():
            raise ValidationError("Username or Password incorrect")
