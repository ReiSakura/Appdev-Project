from flask import Blueprint, render_template, session, redirect, url_for, request, abort, flash
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, validators, PasswordField, EmailField
from wtforms.fields import EmailField
from wtforms_validators import AlphaNumeric
from wtforms.widgets import PasswordInput
from data.database import Database
from data.table import Table
from accounts.customer import Customer
from accounts.admin import Admin
import uuid
from uuid import UUID
import time
import os
from hashlib import sha256
from accounts.customer import Customer

account = Blueprint("account", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))


class UpdateForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1, max=25)])
    password = StringField('Password', [validators.Length(
        min=8, max=30)], widget=PasswordInput(hide_value=False))


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1, max=25)])
    password = PasswordField('Password', [validators.Length(min=1, max=25)])


class RegisterForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=25)])
    email = EmailField('Email', [validators.Length(min=1, max=50)])
    username = StringField(
        'Username', [validators.Length(min=1, max=25), AlphaNumeric()])
    password = PasswordField('Password', [validators.Length(min=8, max=30)])
    address = StringField('Address', [validators.Length(min=1, max=50)])


class AdminRegisterForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=25)])
    email = EmailField('Email', [validators.Length(min=1, max=50)])
    username = StringField(
        'Username', [validators.Length(min=1, max=25), AlphaNumeric()])
    password = PasswordField('Password', [validators.Length(min=8, max=30)])


@account.route('/login', methods=["GET", "POST"])
def login(response=302):
    """
    Login Page
    """
    form = LoginForm()
    if form.validate_on_submit():
        db = Database()
        try:
            users = db.tables["users"]
        except:
            # No point creating new table when registration is requred
            users = Table('users')
        result = None
        for x in users.getColumn('users'):
            if (x.username.lower() == form.username.data.lower()):
                result = x
                break
        if result != None:
            user = result
            if sha256(bytes(form.password.data, 'UTF-8')).hexdigest() == user.password:
                session["user"] = {'username': user.username,
                                   'password': user.password,
                                   'uuid':  user.uuid,
                                   'accounttype': user.accounttype,
                                   'last_entered': user.last_entered
                                   }
                print(session["user"]["uuid"])
                flash(f'Welcome Back {user.username}', 'success')
                if (session["user"]["accounttype"] != "admin"):
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('inventory.get_inventory'))
            else:
                form.password.errors.append(
                    'Username or Password is Incorrect')
        else:
            if (len(form.password.errors) == 0):
                form.password.errors.append(
                    'Username or Password is Incorrect')
    return render_template("login.html", form=form)


@account.route('/register', methods=["GET", "POST"])
def register():
    """
    Register Page
    """
    form = RegisterForm()
    if form.validate_on_submit():
        db = Database()
        try:
            users = db.tables["users"]
        except:
            users = Table("users")
        check = False
        for x in users.getColumn('users'):
            if (x.username == form.username.data):
                check = True
                break
        user = Customer(name=form.name.data, email=form.email.data,  username=form.username.data,
                        password=form.password.data, uuid=uuid.uuid4(), address=form.address.data)
        if (not (check)):
            users.insertRow({"users": user})
        else:
            print("Failed")
            db.close()
            form.username.errors.append('Username already exists')
            return render_template("register.html", form=form, code=401)
        db.tables["users"] = users
        db.close()
        session["user"] = {'username': user.username,
                           'password': user.password,
                           'uuid':  user.uuid,
                           'accounttype': user.accounttype,
                           'last_entered': user.last_entered
                           }
        print("New User")
        return redirect(url_for('home'))
    return render_template("register.html", form=form)


@account.route('/logout', methods=["GET", "POST"])
def logout():
    session["user"] = {'username': 'guest',
                       'password': 'guest',
                       'uuid': uuid.uuid4(),
                       'accounttype': 'guest',
                       'last_entered': time.time()}
    flash("Logged Out", "danger")
    return redirect(url_for('home'))


@account.route('/admin/register', methods=["GET", "POST"])
def adminregister():
    """
    Register Page
    """
    form = AdminRegisterForm()
    if form.validate_on_submit():
        print("validated")
        db = Database()
        try:
            users = db.tables["users"]
        except:
            users = Table("users")
        check = False
        for x in users.getColumn('users'):
            if ('$' + x.username == form.username.data):
                check = True
                break
        user = Admin(email=form.email.data, name=form.name.data, username='$' +
                     form.username.data, password=form.password.data, uuid=uuid.uuid4())
        if (not (check)):
            users.insertRow({"users": user})
        else:
            print("Failed")
            db.close()
            form.username.errors.append('Username already exists')
            return render_template("register.html", form=form, code=401)
        db.tables["users"] = users
        db.close()
        session["user"] = {'username': user.username,
                           'password': user.password,
                           'uuid':  user.uuid,
                           'accounttype': user.accounttype,
                           'last_entered': user.last_entered
                           }
        print("New User")
        return redirect('http://127.0.0.1:5000/inventory')
    return render_template("adminregister.html", form=form)


@account.route('/', methods=["GET", "POST"])
def getaccount():
    """
    Retrieve account details
    """
    db = Database()
    try:
        users = db.tables["users"]
    except:
        users = Table("users")
    users_dict = users.rows
    users_list = []
    for x in users_dict:
        users_list.append(x["users"])
    db.close()

    # print(results)
    return render_template('accountmanage.html', users_list=users_list)


@account.route('/update/<uuid>', methods=["GET", "POST"])
def update(uuid):
    # updates the account details
    form = UpdateForm()
    user_dict = {}
    db = Database()
    try:
        users = db.tables["users"]
    except:
        users = Table("users")
    user = None
    for x in users.rows:
        if (x["users"].uuid == UUID(uuid)):
            user = x["users"]
            if (form.validate_on_submit()):
                users.rows.remove(x)
    if (form.validate_on_submit()):
        user.username = form.username.data
        user.password = form.password.data
        users.insertRow({"users": user})
        db.tables["users"] = users
        flash('User Updated', 'warning')
        return redirect(url_for('accountmanage.getaccount'))
    form.username.data = user.username
    form.password.data = user.password
    db.close()
    return render_template('accmanageupdate.html', form=form)


@account.route('/delete/<uuid>', methods=["POST"])
def delete(uuid):
    # deletes the account
    db = Database()
    try:
        users = db.tables["users"]
    except:
        users = Table("users")
    print(uuid)
    for x in users.rows:
        print(x['users'].uuid)
        if (x['users'].uuid == UUID(uuid)):
            users.rows.remove(x)  # delete

    db.tables["users"] = users
    db.close()

    # print(results)
    return redirect(url_for('account.getaccount'))
