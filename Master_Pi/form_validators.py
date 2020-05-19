from wtforms.validators import ValidationError
import requests

def unique_username(form, field):
    """Ensure that the username is unique

    :param form: the form the user enters details on
    :param field: the field to check for valid data in
    """
    # check if username does not exist in database
    customer = requests.get("http://127.0.0.1:5000/api/customer/username/" + field.data).json()
    if customer:
        raise ValidationError("Username already taken")

def unique_email(form, field):
    """Ensure that the email entered by the user on the form is unique

    :param form: the form the user enters details on
    :param field: the field to check for valid data in
    """
    customer = requests.get("http://127.0.0.1:5000/api/customer/email/" + field.data).json()
    if customer:
        raise ValidationError("Eamil used by another account")

def login_details_correct(form, field):
    """Ensure that the login details entered by the user are correct

    :param form: the form the user enters details on
    :param field: the field to check for valid data in
    """
    if form.username.data and form.password.data:
        data = {"username":form.username.data, "password":form.password.data}
        if not requests.post("http://127.0.0.1:5000/api/customer/verify", data=data).json():
            raise ValidationError("Username or Password incorrect")
