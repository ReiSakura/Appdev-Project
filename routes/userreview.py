# user reviews

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

userreview = Blueprint("userreview", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))


@userreview.route('/', methods=['GET', 'POST'])
def get_userreview():
    '''
    Review page
    '''

    return render_template('review.html')