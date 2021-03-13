from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from .models import Customer


class CustomerRegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password',  validators=[DataRequired(), EqualTo('password')])
    
    country = StringField('Country',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    pincode = StringField('Pincode',validators=[DataRequired()])
    contact = StringField('Contact No',validators=[DataRequired()])

    submit = SubmitField('Register')


    def validate_username(self, username):
        user = Customer.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('That username is taken. Choose a different one')
    
    def validate_email(self, email):
        user = Customer.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('That email is taken. Choose a different one')



class CustomerLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')