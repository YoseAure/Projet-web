from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
                             DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[
                            DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    phone = StringField('Phone', validators=[Length(min=0, max=20)])
    address = StringField('Address', validators=[Length(min=0, max=255)])
    company = StringField('Company', validators=[Length(min=0, max=255)])
    twitter = StringField('Twitter', validators=[Length(min=0, max=255)])
    instagram = StringField('Instagram', validators=[Length(min=0, max=255)])
    facebook = StringField('Facebook', validators=[Length(min=0, max=255)])
    github = StringField('Github', validators=[Length(min=0, max=255)])
    submit = SubmitField('Save Changes')
