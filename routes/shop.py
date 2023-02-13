import uuid
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, send_from_directory, escape, session
from data.database import Database
from data.table import Table
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, validators, FileField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads, IMAGES, UploadSet
from uuid import UUID
import os
import re

shop = Blueprint("shop", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))


@shop.route('/', methods=["GET"])
def get_shop():
    """
    Shows full shop and inventory
    """
    db = Database()
    try:
        table = db.tables["inventory"]
    except KeyError:
        table = Table('imagename', 'name', 'category',
                      'description', 'quantity', 'price', 'productID')
    products = table.rows
    db.close()
    return render_template('shop.html', products=products, acc_type=session["user"]["accounttype"], accounttype=session["user"]["accounttype"])


@shop.route('/product/<productid>', methods=['GET'])
def item(productid):
    db = Database()
    print(productid)
    try:
        table = db.tables["inventory"]
    except KeyError:
        table = Table('imagename', 'name', 'category',
                      'description', 'quantity', 'price', 'productID')
    print(table.rows)
    try:
        # Should have only one item
        result = table.finditem_eq(UUID(productid))[1][0]
    except:
        abort(404)
    return render_template("displayProduct.html", product=result, acc_type=session["user"]["accounttype"], accounttype=session["user"]["accounttype"])
