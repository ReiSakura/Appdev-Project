from flask import Blueprint, Flask, render_template, request, redirect, url_for, send_file, flash
import csv
import os
from .Intermediate import *
from PIL import Image
import secrets
import pandas as pd
import shelve
from .forms import RegisterForm, LoginForm, ProfileForm, AdminLoginForm, CreateAdminForm
from .forms import addproduct, addtocart, updatecart, cnfrmorder, updateProduct, update, feedbackform, FaqForm,remove_user
from datetime import datetime

admin = Blueprint("admin", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))


# function to display admin login page
@admin.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    # create form object
    form = AdminLoginForm()
    # variable to store email and password
    email = None
    password = None
    # if the user presses the submit button
    if request.method == "POST":
        if form.validate():
            # get data from form
            email = request.form['email']
            password = request.form['password']
            # check if email and password is correct
            if validate_admin(email, password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('admin_home'))
            else:
                flash('Email or Password is incorrect', category='danger')
        # if there are errors display them
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'There was an error with logging in: {err_msg}', category='danger')
    return render_template("admin_login.html", form=form)


# function to validate admin login
def validate_admin(email, password):
    try:
        admin_file = shelve.open("admin")
        admins = admin_file['admin']
        is_email = False
        is_password = False
        for admin in admins:
            if email == admin[4]:
                is_email = True
                if password == admin[5]:
                    is_password = True
                    break
        if is_email and is_password:
            admin_file.close()
            return True
        else:
            admin_file.close()
            return False
    except:
        admins = []
        admins.append(['Admin', 'Account',  '+62311 8559959',
                      'M', 'admin@gmail.com', 'admin@', '47010'])
        admin_file['admin'] = admins
        return False


# function to display admin registration page
@admin.route('/admin_registration', methods=['GET', 'POST'])
def create_admin():
    # new variables to store data
    first_name = None
    last_name = None
    phone_no = None
    gender = None
    email_address = None
    password = None
    postal_code = None

    form = CreateAdminForm()
# if the user presses the submit button
    if request.method == "POST":
        # validate form
        if form.validate():
            # get data from form
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone_no = request.form['phone_no']
            gender = request.form['gender']
            email_address = request.form['email_address']
            password = request.form['password']
            postal_code = request.form['postal_code']
            # check if email already exists
            if validate_admin_email(email_address) == False:
                # check if postal code is valid
                if validate_postalcode(postal_code):
                    # create admin
                    add_admin(first_name, last_name, phone_no, gender,
                              email_address, password, postal_code)
                    flash('Admin created successfully!', category='success')

                    return redirect(url_for('admin_home'))
            # display all errors
                else:
                    flash('Invalid postal code ', category='danger')

            else:
                flash('Email already exists', category='danger')

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'There was an error with Registration: {err_msg}', category='danger')
    return render_template("admin_registration.html", form=form)


# function to validate postal code
def validate_postalcode(postalcode):
    postalcode = str(postalcode)
    if len(postalcode) > 6 or len(postalcode) < 4:
        return False
    if not postalcode.isdigit():
        return False
    return True

# function to validate email for admin


def validate_admin_email(email):
    try:
        admin_file = shelve.open("admin")
        admins = admin_file['admin']
        for admin in admins:
            if email == admin[4]:
                return True
        admin_file.close()
        return False
    except:
        admin_file.close()
        return False

# function to add admin


def add_admin(first_name, last_name, phone_no, gender, email_address, password, postal_code):
    try:
        admin_file = shelve.open("admin")
        admins = admin_file['admin']
        admins.append([first_name, last_name, phone_no, gender,
                      email_address, password, postal_code])
        admin_file['admin'] = admins
        admin_file.close()
    except:
        admins = []
        admins.append([first_name, last_name, phone_no, gender,
                      email_address, password, postal_code])
        admin_file['admin'] = admins
        admin_file.close()