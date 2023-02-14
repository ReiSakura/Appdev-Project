# Main Python File for Application(Website)

# from routes.{python-file} import {variable}
# Import routes here
from routes.inventory import inventory
from routes.announcements import announcements
from routes.feedback import feedback
from routes.review import review
from routes.shop import shop
from routes.account import account
from routes.aboutus import aboutus
from routes.userreview import userreview
from routes.userannouncements import userannouncements
from routes.contactus import contactus
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
app.register_blueprint(feedback, url_prefix="/feedback")
app.register_blueprint(review, url_prefix="/review")
app.register_blueprint(shop, url_prefix="/shop")
app.register_blueprint(account, url_prefix="/account")
app.register_blueprint(aboutus, url_prefix="/aboutus")
app.register_blueprint(userannouncements, url_prefix="/Announcements")
app.register_blueprint(contactus, url_prefix="/contactus")
app.register_blueprint(userreview, url_prefix="/review")

admin = ["accountmanage", "contact admin",
         "auth.adminregister", "dashboard", "inventory"]


@app.before_request
def authorizer():
    if (not ("user" in session)):
        print("New User")
        session["user"] = {'username': 'guest',
                           'password': 'guest',
                           'uuid': uuid.uuid4(),
                           'accounttype': 'guest',
                           'last_entered': time.time(),
                           }
    else:
        if (session["user"]["last_entered"] + 24 * 60 * 60 < time.time()):
            session["user"]["last_entered"] = time.time()
    if (request.endpoint):
        for x in admin:
            if (x in request.endpoint):
                if (session["user"]["accounttype"] != "admin"):
                    abort(403)


@app.after_request
def xssprotector(response):
    """
    Protection Headers
    Prevents
    XSS, 
    Man in the Middle,
    clickjacking
    """
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")
