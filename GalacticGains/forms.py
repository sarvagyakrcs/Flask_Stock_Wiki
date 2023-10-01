from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    email = StringField('Email ID', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(max=25)])
    login = SubmitField('Login')


class SignUpForm(FlaskForm):
    email = StringField("Email ID", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(max=25)])
    confirmPassword = PasswordField("Confirm Password", validators=[InputRequired(), Length(max=25)])
    register = SubmitField("Register")
