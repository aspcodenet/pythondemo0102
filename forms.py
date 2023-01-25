from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.fields import IntegerField

class NewCustomerForm(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired()])
    city = StringField('city', validators=[validators.DataRequired()])