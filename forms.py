from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator


class RegistrationForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmer mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Créer mon compte')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')


class EditProfileForm(FlaskForm):
    phone = StringField('Téléphone', validators=[Length(max=20)])
    address = StringField('Adresse', validators=[Length(max=255)])
    city = StringField('Ville', validators=[Length(max=255)])
    postal_code = StringField('Code postal', validators=[Length(max=20)])
    country = StringField('Pays', validators=[Length(max=255)])
    company = StringField('Entreprise', validators=[Length(max=255)])
    twitter = StringField('Twitter', validators=[Length(max=255)])
    instagram = StringField('Instagram', validators=[Length(max=255)])
    facebook = StringField('Facebook', validators=[Length(max=255)])
    github = StringField('Github', validators=[Length(max=255)])
    submit = SubmitField('Sauvegarder')