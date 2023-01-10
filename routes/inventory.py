import uuid
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, send_from_directory, escape
from data.database import Database
from data.table import Table
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators, FileField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads, IMAGES, UploadSet
#from routes.dashboard import update_db
import os
import re

inventory = Blueprint("inventory", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))

# Table display for page
headings = ["Image Name", "Name", "Category", "Description",
            "Quantity", "Price", "Product ID", "Delete", "Modify"]


class productForm(FlaskForm):
    '''
    Form object for database.
    '''
    #FileField('images', validators=[FileRequired()])
    image = FileField('images', validators=[InputRequired()])
    name = StringField('Product Name', [validators.Length(min=1, max=25)])
    category = SelectField('Category', choices=[('Fruits', 'Fruits'), ('Vegetable', 'Vegetable'), (
        'Meat', 'Meat'), ('CannedFood', 'CannedFood'), ('CleaningProducts', 'CleaningProducts')], default='F')
    description = TextAreaField(
        u'Description', [validators.optional(), validators.length(max=200)])
    quantity = IntegerField(
        'Quantity', [validators.NumberRange(min=1, max=99999)])
    price = IntegerField('Price (In Cents)', [
                         validators.NumberRange(min=1, max=99999)])
    addSubmit = SubmitField('Submit')


class quantityForm(FlaskForm):
    '''
    Quanity Form object for database
    '''
    quantity = IntegerField(
        'Quantity', [validators.NumberRange(min=1, max=99999)])


class imageForm(FlaskForm):
    '''
    Image form object for database
    '''
    image = FileField('images')


@inventory.route('/', methods=['GET', 'POST'])
def get_inventory():
    '''
    Main Page
    '''
    # Create table for display
    database = Database()
    try:
        dbtable = database.tables["inventory"]
    except:
        dbtable = Table('imagename', 'name', 'category',
                        'description', 'quantity', 'price', 'productID')
    database.close()
    print("inventory ran")

    form = quantityForm()
    #statTable = update_db()
    #products = displayProduct(statTable["restockMinimum"])
    return render_template('inventory.html')
