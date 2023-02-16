# user announcements

import uuid
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, send_from_directory, escape, session
from data.database import Database
from data.table import Table
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, validators, FileField, IntegerField, SelectField, SubmitField, Form, RadioField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_wtf.file import FileField, FileAllowed
from uuid import UUID
import shelve
import os
import re

user_announce = Blueprint("user_announce", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))


class CreateAnnouncementForm(Form):
    title = StringField('Title', [validators.Length(
        min=1, max=50), validators.DataRequired()])
    content = StringField('Content', [validators.Length(
        min=1, max=200), validators.DataRequired()])
    category = RadioField('Category', choices=[
                          ('G', "General"), ("Ha", "Handwear"), ("N", 'Neckwear'), ("He", "Headwear")], default="G")
    picture = FileField(label="Upload Image", validators=[
                        FileAllowed(['jpg', 'png'])])


class FilterForm(Form):
    filter = SelectField("Filter", choices=[
                         ("G", "General"), ("Ha", "Handwear"), ("He", "Headwear"), ("N", "Neckwear")], default="G")


@user_announce.route('/', methods=['GET', 'POST'])
def get_user_announce():
    '''
    Announcement page
    '''
    # Create the form.
    create_announcement_form = CreateAnnouncementForm(request.form)

    # Validations.
    if request.method == 'POST' and create_announcement_form.validate():
        announcements_dict = {}
        db = shelve.open('announcement.db', 'c')

        try:
            announcements_dict = db['Announcements']
        except:
            print("Error in retrieving Announcements from announcement.db.")

        announcement = Announcement(create_announcement_form.title.data,
                                    create_announcement_form.content.data, create_announcement_form.category.data)
        announcements_dict[announcement.get_announcement_id()] = announcement

        print(announcements_dict)
        db['Announcements'] = announcements_dict

        db.close()

        return redirect(url_for('userannouncements.retrieve_announcements'))
    return render_template('announcements.html', form=create_announcement_form)
