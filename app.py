from flask import Flask, url_for, render_template, session
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
import email_validator
import sqlite3


app = Flask(__name__)
bcrypt = Bcrypt(app)
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

def create_database():
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
         id INTEGER PRIMARY KEY,
         name TEXT,
         email TEXT,
         password TEXT
    );
    ''')
    conn.commit()
    conn.close()

def is_user_name(name):
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    if row is None:
        return False
    else:
        return True

def is_user_email(email):
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    if row is None:
        return False
    else:
        return True
    
def get_password(name):
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return None


def add_user(name, email, password):
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()

def show_db():
     conn = sqlite3.connect('users_data.db')
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM users ")
     rows = cursor.fetchall()
     for row in rows:
        print(row)
     conn.commit()
     conn.close()



@app.route('/register', methods=["GET", "POST"])
def register():
    reg_form = RegForm()
    if reg_form.validate_on_submit():
        if is_user_name(reg_form.name.data):
            return render_template("register.html", form=reg_form, message='Такое имя уже существует')

        if is_user_email(reg_form.email.data):
            return render_template("register.html", form=reg_form, message='Такой emil уже существует')

        name = reg_form.name.data
        email = reg_form.email.data
        password = bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8')
        add_user(name, email, password)
        session['email'] = email
        show_db()
        return render_template("user.html", email=email, name=name)
        
    return render_template("register.html", form=reg_form, message = '')


@app.route('/login', methods=["GET", "POST"])
def login():
    log_form = LogForm()
    if log_form.validate_on_submit():
         name = log_form.name.data
         if is_user_name(name):
            password_db = get_password(name) 
            if password_db is None:
                 return render_template("login.html", form=log_form, message='Пароля нет в базе данных')
            else:
                is_correct = bcrypt.check_password_hash(password_db, log_form.password.data)
                if is_correct:
                    return render_template("user.html", email=session['email'], name=name)
                else: 
                    return  render_template("login.html", form=log_form, message='Пароль не верный')
         else:
             return  render_template("login.html", form=log_form, message='Неверное Имя')
    return render_template("login.html", form=log_form)

if __name__ == "__main__":
    create_database()
    app.run(debug=True, port=8000)