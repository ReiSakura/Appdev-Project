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

account = Blueprint("account", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))

# function to find the profile picture of the user
def find_profile_pic(username):
    try:
        user_file = shelve.open("users")
        users = user_file['users']
        for user in users:
            if user[0] == username:
                return os.path.join(account.config['profile_pics'], user[3])
    except:
        return "default.jpeg"

@account.route('/register', methods=['GET', 'POST'])
def register():
    # creating an instance of the RegisterForm class
    form = RegisterForm()
    # necessary variables to store the user input
    username = None
    email = None
    password1 = None
    password2 = None
    address = None
    postal_code = None
    # if the request method is POST, the form is validated
    if request.method == "POST":
        if form.validate():
            # the user input is stored in the variables
            username = request.form['username']
            email = request.form['email_address']
            password1 = request.form['password1']
            password2 = request.form['password2']
            address = request.form['address']
            postal_code = request.form['postal_code']
            # if the user input is valid, the user is added to the database
            # validation is done in the validate_registration function
            if validate_registration(email, username):
                # the user is added to the database using the add_user function
                add_user(username, email, password1, address, postal_code)
                flash('Account created successfully!', category='success')
                # the user is redirected to the marketplace page
                return redirect(url_for('product', username=username, profile=find_profile_pic(username)))
            # if the user input is invalid, the user is redirected to the registration page again
            else:
                flash('Username or Email already exists', category='danger')
        # the errors are displayed to the user using flash messages
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'There was an error with creating a user: {err_msg}', category='danger')
    # the registration page is rendered
    return render_template('register.html', form=form)


# function which displays the login page
@account.route('/login', methods=['GET', 'POST'])
def login():
    # creating an instance of the LoginForm class
    form = LoginForm()
    # if the request method is GET, the username is retrieved from the url
    if request.method == "GET":
        username = request.args.get('username')
    # if the request method is POST, the form is validated
    if request.method == "POST":
        cart_file = shelve.open("cart")
        cart_file['cart'] = []
        cart_file.close()
        if form.validate():
            # the user input is stored in the variables
            username = request.form['username']
            password = request.form['password']
            # check if the user exists in the database
            if validate_login(username, password):
                flash('Logged in successfully!', category='success')
                # redirecting him to the product page
                return redirect(url_for('product', username=username, profile=find_profile_pic(username)))
            else:
                flash('Username or Password is incorrect', category='danger')
        # if there were errors in the user input, the user is redirected to the login page again
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'There was an error with logging in: {err_msg}', category='danger')
    return render_template('login.html', form=form, username=username, profile=find_profile_pic(username))

