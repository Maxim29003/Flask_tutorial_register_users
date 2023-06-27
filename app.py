from flask import Flask, url_for, render_template
from flask_bcrypt import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
import email_validator
import sqlite3


app = Flask(__name__)
app.secret_key = "nsdfgndflksjgnsdfjlg"

class RegForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email(granular_message=True)])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Register')


class LogForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Register')


@app.route('/register', methods=["GET", "POST"])
def register():
    reg_form = RegForm()
    if reg_form.validate_on_submit():
        print(f"Name:{reg_form.name.data}, E-mail:{reg_form.email.data},Password:{reg_form.password.data}")
    return render_template("register.html", form=reg_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    log_form = LogForm()
    if log_form.validate_on_submit():
         print(f"Name:{log_form.name.data},Password:{log_form.password.data}")
    return render_template("login.html", form=log_form)

if __name__ == "__main__":
    app.run(debug=True)