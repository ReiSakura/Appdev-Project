import uuid
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, send_from_directory, escape, session
from data.Feedback import Feedback
from data.table import Table
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, validators, FileField, IntegerField, SelectField, SubmitField, RadioField, Form
from wtforms.fields import EmailField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads, IMAGES, UploadSet
from uuid import UUID
import shelve
import os
import re
from datetime import date

contactus = Blueprint("contactus", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))

class CreateFeedbackForm(Form):
    firstName = StringField('Name', [validators.Regexp(
        '[a-zA-Z][a-zA-Z ]+[a-zA-Z]$', message="Name must contain only alphabets"), validators.Length(min=1, max=150), validators.DataRequired()])
    category = RadioField('Category', choices=[
                          ('G', "General"), ("P", "Product"), ("T", 'Treatment')], default="G")
    feedback = TextAreaField('Feedback', [validators.DataRequired()])
    status = SelectField('Status(**FOR ADMIN USE**)',
                         choices=[('P', 'PENDING'), ('C', 'CLOSED')], default='P')
    email = EmailField(
        'Email', [validators.Email(), validators.DataRequired()])

@contactus.route('/', methods=['GET', 'POST'])
def createFeedback():
    createFeedbackForm = CreateFeedbackForm(request.form)
    if request.method == 'POST' and createFeedbackForm.validate():
        usersDict = {}
        db = shelve.open('feedstorage.db', 'c')

        try:
            usersDict = db['Feedback']
        except:
            print("Error in retrieving Users from storage.db.")

        feedback = Feedback(createFeedbackForm.firstName.data, createFeedbackForm.email.data, createFeedbackForm.category.data,
                            createFeedbackForm.feedback.data, createFeedbackForm.status.data, date=date.today())
        usersDict[feedback.get_userID()] = feedback
        db['Feedback'] = usersDict
        db.close()

        return redirect(url_for('contactus.get_submission'))
    return render_template('contactUs.html', form=createFeedbackForm)

@contactus.route('/submission', methods=['GET', 'POST'])
def get_submission():
    '''
    SUbmission page
    '''

    return render_template('submission.html')


