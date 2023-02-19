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

accountmanage = Blueprint("accountmanage", __name__, static_folder=os.path.join(
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


@accountmanage.route('/', methods=["GET", "POST"])
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


@accountmanage.route('/update/<uuid>', methods=["GET", "POST"])
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


@accountmanage.route('/delete/<uuid>', methods=["POST"])
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
    return redirect(url_for('accountmanage.getaccount'))


@accountmanage.route('/logout', methods=["GET", "POST"])
def logout():
    session["user"] = {'username': 'guest',
                       'password': 'guest',
                       'uuid': uuid.uuid4(),
                       'accounttype': 'guest',
                       'last_entered': time.time()}
    flash("Logged Out", "danger")
    return redirect(url_for('home'))
