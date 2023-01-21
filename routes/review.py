import uuid
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, send_from_directory, escape
from data.Review import Review
from wtforms import Form, StringField, TextAreaField, validators, FileField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads, IMAGES, UploadSet
import shelve
import os
import re

review = Blueprint("review", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))

class CreateReviewForm(Form):
        first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
        last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
        gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
    default='')
        rating = SelectField('Rating', [validators.DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'),('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')],
    default='5')
        remarks = TextAreaField('Remarks', [validators.Optional()])


@ review.route('/createReview', methods=['GET', 'POST'])
def create_review():
    '''
    Add review page
    '''
    #Create the form.
    create_review_form = CreateReviewForm(request.form)

    #Validations.
    if request.method == 'POST' and create_review_form.validate():
        review_dict = {}
        db = shelve.open('review.db', 'c')

        try:
            review_dict = db['Review']
        except:
            print("Error in retrieving Review from review.db.")

        review = Review(create_review_form.first_name.data, create_review_form.last_name.data, create_review_form.gender.data, create_review_form.rating.data, create_review_form.remarks.data)
        review_dict[review.get_userID()] = review

        print(review_dict)
        db['Review'] = review_dict

        db.close()

        return redirect(url_for('review.retrieve_review'))
    return render_template('createReview.html', form=create_review_form)

@ review.route('/retrieveReview')
def retrieve_review():
    '''
    Retrieve data in review
    '''
    review_dict = {}
    db = shelve.open('review.db', 'r')
    review_dict = db['Review']
    db.close()

    review_list = []
    for key in review_dict:
        review = review_dict.get(key)
        review_list.append(review)

    return render_template('retrieveReview.html', count=len(review_list), review_list=review_list)


@ review.route('/<uuid:id>', methods=['POST'])
def delete_review(id):
    '''
    Delete data in review based on id
    '''
    review_dict = {}
    db = shelve.open('review.db', 'w')
    review_dict = db['Review']

    review_dict.pop(id)

    db['Review'] = review_dict
    db.close()

    return redirect(url_for('review.retrieve_review'))