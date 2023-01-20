# Main Python File for Application(Website)

# from routes.{python-file} import {variable}
# Import routes here
from routes.inventory import inventory
from routes.announcements import announcements

from flask_uploads import configure_uploads, IMAGES, UploadSet
from uuid import UUID
import time
import datetime
import shelve
import os
from flask import Flask, render_template, url_for, session, after_this_request, request, abort, redirect
import uuid
import mimetypes
mimetypes.add_type('application/javascript', '.js')
localpath = os.getcwd()
app = Flask(
    __name__, template_folder=f"{os.getcwd()}/templates", static_folder=f"{os.getcwd()}/static")

# Note just change the secret key by abit to clear all session contents
app.config["SECRET_KEY"] = "mysuperdupersecrethash365tothepowerof369andadditionosfthesecretmatrix420keanureevesss"

# Produict image validations
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOADED_SHOP_DEST'] = os.path.join(localpath, 'static/shop')

shopphotos = UploadSet("shop", IMAGES)
configure_uploads(app, shopphotos)

# Register blueprint for your routes
app.register_blueprint(inventory, url_prefix="/inventory")
app.register_blueprint(announcements, url_prefix="/announcements")

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")
