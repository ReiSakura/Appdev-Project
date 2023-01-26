import uuid
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, send_from_directory, escape
from data.Announcement import Announcement
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, StringField, TextAreaField, validators, FileField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads, IMAGES, UploadSet
import shelve
import os
import re


announcements = Blueprint("announcements", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))


class CreateAnnouncementForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=50), validators.DataRequired()])
    content = StringField('Content', [validators.Length(min=1, max=200), validators.DataRequired()])
    picture = FileField(label="Upload Image", validators=[FileAllowed(['jpg','png'])])


@ announcements.route('/createAnnouncement', methods=['GET', 'POST'])
def create_announcements():
    '''
    Add announcements page
    '''
    #Create the form.
    create_announcement_form = CreateAnnouncementForm(request.form)

    #Validations.
    if request.method == 'POST' and create_announcement_form.validate():
        announcements_dict = {}
        db = shelve.open('announcement.db', 'c')

        try:
            announcements_dict = db['Announcements']
        except:
            print("Error in retrieving Announcements from announcement.db.")

        announcement = Announcement(create_announcement_form.title.data, create_announcement_form.content.data)
        announcements_dict[announcement.get_announcement_id()] = announcement

        print(announcements_dict)
        db['Announcements'] = announcements_dict

        db.close()

        return redirect(url_for('announcements.retrieve_announcements'))
    return render_template('createAnnouncement.html', form=create_announcement_form)

@ announcements.route('/retrieveAnnouncement')
def retrieve_announcements():
    '''
    Retrieve data in announcements
    '''
    announcements_dict = {}
    db = shelve.open('announcement.db', 'r')
    announcements_dict = db['Announcements']
    db.close()

    announcements_list = []
    for key in announcements_dict:
        announcement = announcements_dict.get(key)
        announcements_list.append(announcement)

    return render_template('retrieveAnnouncement.html', count=len(announcements_list), announcements_list=announcements_list)

@ announcements.route('/edit/<uuid:id>/', methods=['GET', 'POST'])
def update_announcement(id):
    '''
    Edit page
    '''
    update_announcement_form = CreateAnnouncementForm(request.form)
    if request.method == 'POST' and update_announcement_form.validate():
        announcements_dict = {}
        db = shelve.open('announcement.db', 'w')
        announcements_dict = db['Announcements']

        announcement = announcements_dict.get(id)
        announcement.set_title(update_announcement_form.title.data)
        announcement.set_content(update_announcement_form.content.data)

        db['Announcements'] = announcements_dict
        db.close()

        return redirect(url_for('announcements.retrieve_announcements'))
    else:
        announcements_dict = {}
        db = shelve.open('announcement.db', 'r')
        announcements_dict = db['Announcements']
        db.close()

        announcement = announcements_dict.get(id)
        update_announcement_form.title.data = announcement.get_title()
        update_announcement_form.content.data = announcement.get_content()

        return render_template('updateAnnouncement.html', form=update_announcement_form)

@ announcements.route('/<uuid:id>', methods=['POST'])
def delete_announcement(id):
    '''
    Delete data in announcement based on id
    '''
    announcements_dict = {}
    db = shelve.open('announcement.db', 'w')
    announcements_dict = db['Announcements']

    announcements_dict.pop(id)

    db['Announcements'] = announcements_dict
    db.close()

    return redirect(url_for('announcements.retrieve_announcements'))
