import uuid
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, send_from_directory, escape
from data.database import Database
from data.table import Table
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators, FileField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads, IMAGES, UploadSet
import os
import re

inventory = Blueprint("inventory", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))

# File path for images
images = UploadSet(f"shop", IMAGES, default_dest="shop")

# Table display for page
headings = ["Image", "Name", "Category", "Description",
            "Quantity", "Price", "Product ID", "Delete", "Update"]

localpath = os.getcwd()


class productForm(FlaskForm):
    '''
    Form object for database.
    '''
    #FileField('images', validators=[FileRequired()])
    image = FileField('images', validators=[InputRequired()])
    name = StringField('Product Name', [validators.Length(min=1, max=30)])
    category = SelectField('Category', choices=[('Neckwear', 'Neckwear'), ('Earwear', 'Earwear'), ('Handwear', 'Handwear')], default='Neckwear')
    description = TextAreaField(
        u'Description', [validators.optional(), validators.length(max=200)])
    quantity = IntegerField(
        'Quantity', [validators.NumberRange(min=1, max=999)])
    price = IntegerField('Price (In Cents)', [
                         validators.NumberRange(min=1, max=9999999)])
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

    form = quantityForm()
    #statTable = update_db()
    #products = displayProduct(statTable["restockMinimum"])

    return render_template('inventory.html', headings=headings, data=dbtable.rows, form=form)


@inventory.route('/add', methods=['GET', 'POST'])
def add_inventory():
    '''
    Add products page
    '''
    # Create the form.
    form = productForm()

    # Validations.
    if form.addSubmit.data and form.validate_on_submit():
        # Create database.
        db = Database()
        try:
            table = db.tables["inventory"]
        except:
            table = Table('imagename', 'name', 'category',
                          'description', 'quantity', 'price', 'productID')

        # Save the image.
        if form.image.data.filename != '':
            filename = images.save(form.image.data)

        # Find duplicate product name and images
        if form.name.data not in table.getColumn("name"):
            if form.image.data.filename not in table.getColumn("imagename"):
                product = {"imagename": request.files["image"].filename.replace(" ", "_").replace('(', '').replace(')', ''), "name": escape(
                    form.name.data), "category": form.category.data, "description": escape(form.description.data), "quantity": int(form.quantity.data), "price": form.price.data, "productID": uuid.uuid4()}
                table.insertRow(product)
                # Add product into database.
                db.tables["inventory"] = table
            else:
                return "Image existed"
        else:
            # Raise error when product name exist cant update the html
            #form.name.errors.append('Product already existed.')

            return "Product Name existed"

        db.close()
        flash('Product Added', 'success')
        return redirect('/inventory/')

    return render_template('addproduct.html', form=form)


@inventory.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_inventory(index):
    '''
    Edit Page
    '''
    categories = ['Neckwear', 'Earwear', 'Handwear']
    form = productForm()
    database = Database()
    try:
        dbtable = database.tables["inventory"]
    except:
        dbtable = Table('imagename', 'name', 'category',
                        'description', 'quantity', 'price', 'productID')
    database.close()

    image = imageForm()

    # Assign the data in a variable
    data = dbtable.rows[index]

    if request.method == 'POST':
        # Create database.
        db = Database()
        try:
            table = db.tables["inventory"]
        except:
            table = Table('imagename', 'name', 'category',
                          'description', 'quantity', 'price', 'productID')

        # Checks if new image is added
        if image.image.data.filename != '':
            # Save the image.
            filename = images.save(form.image.data)

            # Check if image exist
            if image.image.data.filename not in dbtable.getColumn("imagename"):
                product = {"imagename": filename, "name": escape(form.name.data), "category": request.form["category"], "description": escape(
                    request.form["description"]), "quantity": form.quantity.data, "price": form.price.data, "productID": uuid.uuid4()}
        else:
            product = {"imagename": data["imagename"], "name": escape(form.name.data), "category": request.form["category"], "description": escape(
                request.form["description"]), "quantity": form.quantity.data, "price": form.price.data, "productID": uuid.uuid4()}

        # update edited products
        print(product)
        table.insertRow(product)  # Add product into database.
        table.rows.remove(table.rows[index])
        db.tables["inventory"] = table
        db.close()

        flash('Edited Product', 'warning')
        # Return success page next time.
        return redirect(url_for('inventory.get_inventory'))

    return render_template('inventoryEdit.html', form=form, product=data, category=categories, image=image)


@inventory.route('/<int:index>', methods=['POST'])
def deleteDb(index):
    '''
    Delete data in inventory based on index
    '''
    if request.method == "POST":
        db = Database()
        try:
            table = db.tables["inventory"]
        except:
            table = Table('imagename', 'name', 'category',
                          'description', 'quantity', 'price', 'productID')

        table.rows.pop(index)

        db.tables["inventory"] = table
        db.close()
        flash('Product deleted', 'danger')
        return redirect(url_for('inventory.get_inventory'))

    return "Failed to delete"
