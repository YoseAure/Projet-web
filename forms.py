from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator


class RegistrationForm(FlaskForm):
    first_name = StringField('Prénom', validators=[
                             DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Nom', validators=[
                            DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[
                             DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmer mot de passe', validators=[
                                     DataRequired(), EqualTo('Mot de passe')])
    submit = SubmitField('Créer mon compte')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('connexion')

class EditProfileForm(FlaskForm):
    phone = StringField('Téléphone', validators=[Length(min=0, max=20)])
    address = StringField('Addresse', validators=[Length(min=0, max=255)])
    company = StringField('Entreprise', validators=[Length(min=0, max=255)])
    twitter = StringField('Twitter', validators=[Length(min=0, max=255)])
    instagram = StringField('Instagram', validators=[Length(min=0, max=255)])
    facebook = StringField('Facebook', validators=[Length(min=0, max=255)])
    github = StringField('Github', validators=[Length(min=0, max=255)])
    submit = SubmitField('Sauvegarder')
