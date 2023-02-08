from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.fields import IntegerField, SelectField

def emailContains(form, field):
    if not field.data.endswith('.se'):
        raise ValidationError('Måste sluta på .se dummer')

class WithdrawForm(FlaskForm):
    #todo icke negativt belopp
    amount = IntegerField('amount', validators=[validators.DataRequired(), validators.NumberRange(min=1,max=1000000)])


class NewCustomerForm(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired(), emailContains])
    city = StringField('city', validators=[validators.DataRequired()])
    age= IntegerField('age')
    countryCode = SelectField('countryCode',choices=[('SE','+46'),('NO','+41'),('FI','+42')])