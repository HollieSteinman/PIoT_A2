from wtforms.validators import ValidationError
import requests

def unique_username(form, field):
    """Ensure that the username is unique

    :param form: the form the user enters details on
    :param field: the field to check for valid data in
    """
    # check if username does not exist in database
    user = requests.get("http://127.0.0.1:5000/api/user/username/" + field.data).json()
    if user:
        raise ValidationError("Username already taken")

def valid_password(form, field):
    if len(field.data) < 6:
        raise ValidationError("Password must be at least 6 characters long")

def unique_email(form, field):
    """Ensure that the email entered by the user on the form is unique

    :param form: the form the user enters details on
    :param field: the field to check for valid data in
    """
    user = requests.get("http://127.0.0.1:5000/api/user/email/" + field.data).json()
    if user:
        raise ValidationError("Eamil used by another account")

def login_details_correct(form, field):
    """Ensure that the login details entered by the user are correct

    :param form: the form the user enters details on
    :param field: the field to check for valid data in
    """
    if form.username.data and form.password.data:
        data = {"username":form.username.data, "password":form.password.data}
        if not requests.post("http://127.0.0.1:5000/api/user/verify", data=data).json():
            raise ValidationError("Username or Password incorrect")

def valid_updated_username(form, field):
    if form.user_id.data:
        user = requests.get("http://127.0.0.1:5000/api/user/"+form.user_id.data).json()
        if user["username"] != field.data:
            unique_username(form, field)

def valid_updated_email(form, field):
    if form.user_id.data:
        user = requests.get("http://127.0.0.1:5000/api/user/"+form.user_id.data).json()
        if user["email"] != field.data:
            unique_email(form, field)