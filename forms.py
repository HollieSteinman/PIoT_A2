from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from form_validators import unique_username, unique_email, login_details_correct

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In', validators=[login_details_correct])

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), unique_username])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired(), Email(), unique_email])
    submit = SubmitField('Register')
