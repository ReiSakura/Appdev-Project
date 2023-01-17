import uuid
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, send_from_directory, escape
from data.database import Database
from data.table import Table
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators, FileField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads, IMAGES, UploadSet
from .database import db
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
    # FileField('images', validators=[FileRequired()])
    image = FileField('images', validators=[InputRequired()])
    name = StringField('Product Name', [validators.Length(min=1, max=30)])
    category = SelectField('Category', choices=[('Neckwear', 'Neckwear'), (
        'Earwear', 'Earwear'), ('Handwear', 'Handwear')], default='Neckwear')
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


class products(db.Model):
    id = db.Column('product_id', db.Integer, primary_key=True)
    imagename = db.Column(db.String(100))
    name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, imagename, name, category, description, quantity, price):
        self.imagename = imagename
        self.name = name
        self.category = category
        self.description = description
        self.quantity = quantity
        self.price = price


def test_func():
    """
    Test function for adding products
    """
    product123 = products("test", "test",
                          "test", "test", 123, 123)
    db.create_all()
    db.session.add(product123)
    db.session.commit()
    print(products.query.all()[0].id)


@inventory.route('/', methods=['GET', 'POST'])
def get_inventory():
    '''
    Main Page
    '''
    return render_template('inventory.html', headings=headings, data=products.query.all(), form=quantityForm())


@ inventory.route('/add', methods=['GET', 'POST'])
def add_inventory():
    '''
    Add products page
    '''
    # Create the form.
    form = productForm()

    # Validations.
    if form.addSubmit.data and form.validate_on_submit():
        # Save the image.
        if form.image.data.filename != '':
            filename = images.save(form.image.data)

        # Find duplicate product name and images
        if len(products.query.filter_by(name=form.name.data).all()) == 0:
            if len(products.query.filter_by(imagename=form.image.data.filename).all()) == 0:
                product = products(request.files["image"].filename.replace(
                    " ", "_").replace('(', '').replace(')', ''), escape(
                    form.name.data), form.category.data, escape(form.description.data), int(form.quantity.data), form.price.data)
                # Add product into database.
                db.create_all()
                db.session.add(product)
                db.session.commit()
            else:
                return "Image existed"
        else:
            # Raise error when product name exist cant update the html
            # form.name.errors.append('Product already existed.')

            return "Product Name existed"

        flash('Product Added', 'success')
        return redirect('/inventory/')

    return render_template('addproduct.html', form=form)


@ inventory.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_inventory(id):
    '''
    Edit Page
    '''
    categories = ['Neckwear', 'Earwear', 'Handwear']
    form = productForm()

    image = imageForm()

    # Assign the data in a variable
    data = db.get_or_404(products, id)

    if request.method == 'POST':
        # Checks if new image is added
        if image.image.data.filename != '':
            # Save the image.
            filename = images.save(form.image.data)

        # update edited products
        # Add product into database.
        data.imagename = request.files["image"].filename.replace(
            " ", "_").replace('(', '').replace(')', '')
        data.name = escape(
            form.name.data)
        data.description = escape(form.description.data)
        data.quantity = int(form.quantity.data)
        data.price = form.price.data
        db.session.commit()
        flash('Edited Product', 'warning')
        # Return success page next time.
        return redirect(url_for('inventory.get_inventory'))

    return render_template('inventoryEdit.html', form=form, product=data, category=categories, image=image)


@inventory.route('/<int:id>', methods=['POST'])
def deleteDb(id):
    '''
    Delete data in inventory based on id
    '''
    if request.method == "POST":
        product = db.get_or_404(products, id)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('inventory.get_inventory'))

    return "Failed to delete"
