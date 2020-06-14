from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, IntegerField, DecimalField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, NumberRange
from form_validators import unique_username, unique_email, login_details_correct, valid_password, valid_updated_username, valid_updated_email

class LoginForm(FlaskForm):
    """Login form structured as a flask form
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In', validators=[login_details_correct])

class RegisterForm(FlaskForm):
    """Registration form structured as a flask form
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), unique_username])
    password = PasswordField('Password', validators=[DataRequired(), valid_password])
    email = EmailField("Email Address", validators=[DataRequired(), Email(), unique_email])
    submit = SubmitField('Register')

class CarsSearchForm(FlaskForm):
    choices = [("", "Select a car property to search"), ("make", "Make"), ("model", "Model"), ("body_type", "Body Type"), ("colour", "Colour"), ("seats", "Seats"), ("cost_per_hour", "Price Per Hour")]
    search_property = SelectField('property', choices=choices, validators=[DataRequired()])
    search = StringField('Search', validators=[DataRequired()], render_kw={"placeholder": "Search..."})
    submit = SubmitField('Search')

class AllCarsSearchForm(CarsSearchForm):
    choices = [("", "Select a car property to search"), ("car_id", "ID"), ("make", "Make"), ("model", "Model"), ("body_type", "Body Type"), ("colour", "Colour"), ("seats", "Seats"), ("cost_per_hour", "Price Per Hour"), ("status", "Status")]
    search_property = SelectField('property', choices=choices, validators=[DataRequired()])

class UsersSearchForm(FlaskForm):
    choices = [("", "Select a user property to search"), ("user_id", "ID"), ("first_name", "First Name"), ("last_name", "Last Name"), ("username", "Username"), ("email", "Email"), ("type", "Type")]
    search_property = SelectField('property', choices=choices, validators=[DataRequired()])
    search = StringField('Search', validators=[DataRequired()], render_kw={"placeholder": "Search..."})
    submit = SubmitField('Search')

class EditUserForm(FlaskForm):
    user_id = HiddenField("user_id")
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired(), valid_updated_username])
    email = EmailField("Email Address", validators=[DataRequired(), Email(), valid_updated_email])
    choices = [("customer", "customer"), ("admin", "admin"), ("manager", "manager"), ("engineer", "engineer")]
    user_type = SelectField("Type", choices=choices, validators=[DataRequired()])
    submit = SubmitField('Save')

    def fill_data(self, user):
        self.user_id.data = user["user_id"]
        self.first_name.data = user["first_name"]
        self.last_name.data = user["last_name"]
        self.username.data = user["username"]
        self.email.data = user["email"]
        self.user_type.data = user["user_type"]

class EditCarForm(FlaskForm):
    car_id = HiddenField("car_id")
    choices = [("available", "available"), ("unavailable", "unavailable")]
    status = SelectField("Status", choices=choices)
    make = StringField("Make", validators=[DataRequired()])
    model = StringField("Model", validators=[DataRequired()])
    body_type = StringField("Body Type", validators=[DataRequired()])
    colour = StringField("Colour", validators=[DataRequired()])
    seats = IntegerField("Seats", validators=[DataRequired(), NumberRange(min=1, message="There must be at least 1 seat")])
    cost_per_hour = DecimalField("Cost Per Hour", validators=[DataRequired(), NumberRange(min=0, message="Cost per hour cannot be negative")])
    submit = SubmitField('Save')

    def fill_data(self, car):
        self.car_id.data = car["car_id"]
        self.status.data = car["status"]
        self.make.data = car["make"]
        self.model.data = car["model"]
        self.body_type.data = car["body_type"]
        self.colour.data = car["colour"]
        self.seats.data = car["seats"]
        self.cost_per_hour.data = car["cost_per_hour"]

class ReportIssueForm(FlaskForm):
    car_id = HiddenField("car_id")
    description = TextAreaField("Description", validators=[DataRequired()])
    choices = [("unresolved", "unresolved"), ("resolved", "resolved")]
    status = SelectField("Status", choices=choices, validators=[DataRequired()])
    engineer_id = SelectField("Engineer", choices=[("", "Select an engineer")], validators=[DataRequired()], validate_choice=False)
    submit = SubmitField('Submit Report')

    def fill_data(self, car_id, engineers):
        self.car_id.data = car_id
        for engineer in engineers:
            option = (engineer["user_id"], "{} - {} {}".format(engineer["username"], engineer["first_name"], engineer["last_name"]))
            self.engineer_id.choices.append(option)
