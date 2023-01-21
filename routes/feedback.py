import uuid
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, send_from_directory, escape
from data.Feedback import Feedback
from data.Filter import Filter
from wtforms import Form, StringField, RadioField, TextAreaField, validators, FileField, IntegerField, SelectField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads, IMAGES, UploadSet
import shelve
import os
import re
from datetime import date

feedback = Blueprint("feedback", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))


class CreateFeedbackForm(Form):
    firstName = StringField('Name', [validators.Regexp('[a-zA-Z][a-zA-Z ]+[a-zA-Z]$', message="Name must contain only alphabets"),validators.Length (min = 1, max = 150), validators.DataRequired()])
    category = RadioField('Category', choices = [('G', "General"), ("P", "Product"), ("T", 'Treatment')], default= "G")
    feedback = TextAreaField('Feedback', [validators.DataRequired()])
    status = SelectField('Status(**FOR ADMIN USE**)', choices = [('P', 'PENDING'), ('C', 'CLOSED')], default= 'P')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])

class UpdateFeedbackForm(Form):
    firstName = StringField('Name', [validators.Length (min = 1, max = 150), validators.Optional()])
    category = RadioField('Category', choices = [('G', "General"), ("P", "Product"), ("T", 'Treatment')], default= "G")
    feedback = TextAreaField('Feedback', [validators.Optional()])
    status = SelectField('Status(**FOR ADMIN USE**)', choices = [('P', 'PENDING'), ('C', 'CLOSED')], default= '')
    email = EmailField('Email', [validators.Email(), validators.Optional()])

class FilterForm(Form):
    filter = SelectField("Filter", choices= [("", ""), ("Pending", "Pending"), ("Closed", "Closed")], default="")


@ feedback.route('/createFeedback', methods = ['GET', 'POST'])
def createFeedback():
    createFeedbackForm = CreateFeedbackForm(request.form)
    if request.method == 'POST' and createFeedbackForm.validate():
        usersDict = {}
        db = shelve.open('feedstorage.db', 'c')

        try:
            usersDict = db['Feedback']
        except:
            print("Error in retrieving Users from storage.db.")

        feedback = Feedback(createFeedbackForm.firstName.data, createFeedbackForm.email.data, createFeedbackForm.category.data, createFeedbackForm.feedback.data, createFeedbackForm.status.data, date= date.today())
        usersDict[feedback.get_userID()] = feedback
        db['Feedback'] = usersDict
        db.close()

        return redirect(url_for('feedback.retrieveFeedback'))
    return render_template('createFeedback.html', form = createFeedbackForm)


@ feedback.route('/retrieveFeedback', methods=['GET', 'POST'])
def retrieveFeedback():
    filterForm = FilterForm(request.form)
    feedbackDict = {}
    db = shelve.open('feedstorage.db', 'r')
    feedbackDict = db['Feedback']
    db.close()

    feedbackList = []
    for key in feedbackDict:
        feedback = feedbackDict.get(key)
        feedbackList.append(feedback)

    if request.method  == "POST" and filterForm.validate():
        filter_variable = filterForm.filter.data
        if filter_variable == "":
            return redirect(url_for('feedback.retrieveFeedback'))
        elif filter_variable == "Pending":
            return redirect(url_for('feedback.filterPending'))
        elif filter_variable == "Closed":
            return redirect(url_for('feedback.filterClosed'))

    return render_template('retrieveFeedback.html', feedbackList = feedbackList, count = len(feedbackList), form = filterForm)


@ feedback.route('/updateFeedback/<uuid:id>/', methods = ['GET', 'POST'])
def updateFeedback(id):
    updateFeedbackForm = UpdateFeedbackForm(request.form)
    if request.method == 'POST' and updateFeedbackForm.validate():
        userDict = {}
        db = shelve.open('feedstorage.db', 'w')
        userDict = db['Feedback']

        feedback = userDict.get(id)
        feedback.set_status(updateFeedbackForm.status.data)

        db['Feedback'] = userDict
        db.close()

        return redirect(url_for('feedback.retrieveFeedback'))
    else:
        userDict = {}
        db = shelve.open('feedstorage.db', 'r')
        userDict = db['Feedback']
        db.close()

        feedback = userDict.get(id)
        updateFeedbackForm.firstName.data = feedback.get_firstName()
        updateFeedbackForm.email.data = feedback.get_email()
        updateFeedbackForm.category.data = feedback.get_category()
        updateFeedbackForm.feedback.data = feedback.get_feedback()
        updateFeedbackForm.status.data = feedback.get_status()

        return render_template('updateFeedback.html', form = updateFeedbackForm)


#closed route
@ feedback.route('/filterClosed', methods =['GET', 'POST'])
def filterClosed():
    filterForm = FilterForm(request.form)
    feedbackDict = {}
    db = shelve.open('feedstorage.db', 'r')
    feedbackDict = db['Feedback']
    db.close()

    feedbackList = []
    closedList = []

    for key in feedbackDict:
        feedback = feedbackDict.get(key)
        feedbackList.append(feedback)
        if feedback.get_status() == "C":
            closedList.append(feedback)

    if request.method  == "POST" and filterForm.validate():
        filter_variable = filterForm.filter.data
        if filter_variable == "":
            return redirect(url_for('feedback.retrieveFeedback'))
        elif filter_variable == "Pending":
            return redirect(url_for('feedback.filterPending'))
        elif filter_variable == "Closed":
            return redirect(url_for('feedback.filterClosed'))

    return render_template('filterClosed.html', feedbackList = feedbackList, count = len(feedbackList), form = filterForm, closedList = closedList, ccount = len(closedList))

#pending route
@ feedback.route('/filterPending', methods = ['POST', 'GET'])
def filterPending():
    filterForm = FilterForm(request.form)
    feedbackDict = {}
    db = shelve.open('feedstorage.db', 'r')
    feedbackDict = db['Feedback']
    db.close()

    feedbackList = []
    pendingList = []

    for key in feedbackDict:
        feedback = feedbackDict.get(key)
        feedbackList.append(feedback)
        if feedback.get_status() == "P":
            pendingList.append(feedback)

    if request.method  == "POST" and filterForm.validate():
        filter_variable = filterForm.filter.data
        if filter_variable == "":
            return redirect(url_for('feedback.retrieveFeedback'))
        elif filter_variable == "Pending":
            return redirect(url_for('feedback.filterPending'))
        elif filter_variable == "Closed":
            return redirect(url_for('feedback.filterClosed'))

    return render_template('filterPending.html', feedbackList = feedbackList, count = len(feedbackList), form = filterForm, pendingList = pendingList, pcount = len(pendingList))


#Statistics Breakdown
@ feedback.route('/Stats')
def Stats():
    db = shelve.open('feedstorage.db', 'r')
    countDict = db['Feedback']
    db.close()
    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')

    TotalList = []
    JanList = []
    FebList = []
    MarList = []
    AprList = []
    MayList = []
    JunList = []
    JulList = []
    AugList = []
    SepList = []
    OctList = []
    NovList = []
    DecList = []

    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')
        TotalList.append(count)
        if datesplit[1] == '01':
           JanList.append(count)
        elif datesplit[1] == '02':
            FebList.append(count)
        elif datesplit[1] == '03':
            MarList.append(count)
        elif datesplit[1] == '04':
            AprList.append(count)
        elif datesplit[1] == '05':
            MayList.append(count)
        elif datesplit[1] == '06':
            JunList.append(count)
        elif datesplit[1] == '07':
            JulList.append(count)
        elif datesplit[1] == '08':
            AugList.append(count)
        elif datesplit[1] == '09':
            SepList.append(count)
        elif datesplit[1] == '10':
            OctList.append(count)
        elif datesplit[1] == '11':
            NovList.append(count)
        elif datesplit[1]:
            DecList.append(count)

    return render_template('Stats.html', TotalList = TotalList, JanList = JanList, FebList = FebList, MarList = MarList, AprList = AprList, MayList = MayList, JunList = JunList, JulList = JulList, AugList = AugList, SepList = SepList, OctList = OctList, NovList = NovList, DecList = DecList,
                           count = len(TotalList), jancount = len(JanList), febcount = len(FebList), marcount = len(MarList), aprcount = len(AprList), maycount = len(MayList), juncount = len(JunList), julcount = len(JulList), augcount = len(AugList), sepcount = len(SepList), octcount = len(OctList), novcount = len(NovList), deccount = len(DecList))



@ feedback.route('/StatGraph')
def Stats1():
    bar_labels = labels
    bar_values = values
    db = shelve.open('feedstorage.db', 'r')
    countDict = db['Feedback']
    db.close()

#overall
    TotalList = []
    JanList = []
    FebList = []
    MarList = []
    AprList = []
    MayList = []
    JunList = []
    JulList = []
    AugList = []
    SepList = []
    OctList = []
    NovList = []
    DecList = []

#general
    JanGenList = []
    FebGenList = []
    MarGenList = []
    AprGenList = []
    MayGenList = []
    JunGenList = []
    JulGenList = []
    AugGenList = []
    SepGenList = []
    OctGenList = []
    NovGenList = []
    DecGenList = []

#Products
    JanProdList = []
    FebProdList = []
    MarProdList = []
    AprProdList = []
    MayProdList = []
    JunProdList = []
    JulProdList = []
    AugProdList = []
    SepProdList = []
    OctProdList = []
    NovProdList = []
    DecProdList = []

#Treatment
    JanTreatList = []
    FebTreatList = []
    MarTreatList = []
    AprTreatList = []
    MayTreatList = []
    JunTreatList = []
    JulTreatList = []
    AugTreatList = []
    SepTreatList = []
    OctTreatList = []
    NovTreatList = []
    DecTreatList = []

    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')
        TotalList.append(count)
        cat = str(count.get_category())

        if datesplit[1] == '01':
            JanList.append(count)
        elif datesplit[1] == '02':
            FebList.append(count)
        elif datesplit[1] == '03':
            MarList.append(count)
        elif datesplit[1] == '04':
            AprList.append(count)
        elif datesplit[1] == '05':
            MayList.append(count)
        elif datesplit[1] == '06':
            JunList.append(count)
        elif datesplit[1] == '07':
            JulList.append(count)
        elif datesplit[1] == '08':
            AugList.append(count)
        elif datesplit[1] == '09':
            SepList.append(count)
        elif datesplit[1] == '10':
            OctList.append(count)
        elif datesplit[1] == '11':
            NovList.append(count)
        elif datesplit[1]:
            DecList.append(count)

        #generalList
        if datesplit[1] == '01' and cat == 'G':
            JanGenList.append(count)
        elif datesplit[1] == '02' and cat == 'G':
            FebGenList.append(count)
        elif datesplit[1] == '03' and cat == 'G':
            MarGenList.append(count)
        elif datesplit[1] == '04' and cat == 'G':
            AprGenList.append(count)
        elif datesplit[1] == '05' and cat == 'G':
            MayGenList.append(count)
        elif datesplit[1] == '06' and cat == 'G':
            JunGenList.append(count)
        elif datesplit[1] == '07' and cat == 'G':
            JulGenList.append(count)
        elif datesplit[1] == '08' and cat == 'G':
            AugGenList.append(count)
        elif datesplit[1] == '09' and cat == 'G':
            SepGenList.append(count)
        elif datesplit[1] == '10' and cat == 'G':
            OctGenList.append(count)
        elif datesplit[1] == '11' and cat == 'G':
            NovGenList.append(count)
        elif datesplit[1] == '12' and cat == 'G':
            DecGenList.append(count)


        #ProductList
        if datesplit[1] == '01' and cat == 'P':
            JanProdList.append(count)
        elif datesplit[1] == '02' and cat == 'P':
            FebProdList.append(count)
        elif datesplit[1] == '03' and cat == 'P':
            MarProdList.append(count)
        elif datesplit[1] == '04' and cat == 'P':
            AprProdList.append(count)
        elif datesplit[1] == '05' and cat == 'P':
            MayProdList.append(count)
        elif datesplit[1] == '06' and cat == 'P':
            JunProdList.append(count)
        elif datesplit[1] == '07' and cat == 'P':
            JulProdList.append(count)
        elif datesplit[1] == '08' and cat == 'P':
            AugProdList.append(count)
        elif datesplit[1] == '09' and cat == 'P':
            SepProdList.append(count)
        elif datesplit[1] == '10' and cat == 'P':
            OctProdList.append(count)
        elif datesplit[1] == '11' and cat == 'P':
            NovProdList.append(count)
        elif datesplit[1] == '12' and cat == 'P':
            DecProdList.append(count)


        #TreatmentList
        if datesplit[1] == '01' and cat == 'T':
            JanTreatList.append(count)
        elif datesplit[1] == '02' and cat == 'T':
            FebTreatList.append(count)
        elif datesplit[1] == '03' and cat == 'T':
            MarTreatList.append(count)
        elif datesplit[1] == '04' and cat == 'T':
            AprTreatList.append(count)
        elif datesplit[1] == '05' and cat == 'T':
            MayTreatList.append(count)
        elif datesplit[1] == '06' and cat == 'T':
            JunTreatList.append(count)
        elif datesplit[1] == '07' and cat == 'T':
            JulTreatList.append(count)
        elif datesplit[1] == '08' and cat == 'T':
            AugTreatList.append(count)
        elif datesplit[1] == '09' and cat == 'T':
            SepTreatList.append(count)
        elif datesplit[1] == '10' and cat == 'T':
            OctTreatList.append(count)
        elif datesplit[1] == '11' and cat == 'T':
            NovTreatList.append(count)
        elif datesplit[1] == '12' and cat == 'T':
            DecTreatList.append(count)

    return render_template('StatGraph.html', title = 'Feedback - Statistics(Graph)', max = 20, labels = bar_labels, values = bar_values, TotalList = TotalList, JanList = JanList, FebList = FebList, MarList = MarList, AprList = AprList, MayList = MayList, JunList = JunList, JulList = JulList, AugList = AugList, SepList = SepList, OctList = OctList, NovList = NovList, DecList = DecList,
                           count = len(TotalList), jancount = len(JanList), febcount = len(FebList), marcount = len(MarList), aprcount = len(AprList), maycount = len(MayList), juncount = len(JunList), julcount = len(JulList), augcount = len(AugList), sepcount = len(SepList), octcount = len(OctList), novcount = len(NovList), deccount = len(DecList),
                           JanGenList = JanGenList, FebGenList = FebGenList, MarGenList = MarGenList, AprGenList = AprGenList, MayGenList = MayGenList, JunGenList = JunGenList, JulGenList = JulGenList, AugGenList = AugGenList, SepGenList = SepGenList, OctGenList = OctGenList, NovGenList = NovGenList, DecGenList = DecGenList,
                            jangencount = len(JanGenList), febgencount = len(FebGenList), margencount = len(MarGenList), aprgencount = len(AprGenList), maygencount = len(MayGenList), jungencount = len(JunGenList), julgencount = len(JulGenList), auggencount = len(AugGenList), sepgencount = len(SepGenList), octgencount = len(OctGenList), novgencount = len(NovGenList), decgencount = len(DecGenList),
                           JanProdList = JanProdList, FebProdList = FebProdList, MarProdList = MarProdList, AprProdList = AprProdList, MayProdList = MayProdList, JunProdList = JunProdList, JulProdList = JulProdList, AugProdList = AugProdList, SepProdList = SepProdList, OctProdList = OctProdList, NovProdList = NovProdList, DecProdList = DecProdList,
                            janprodcount = len(JanProdList), febprodcount = len(FebProdList), marprodcount = len(MarProdList), aprprodcount = len(AprProdList), mayprodcount = len(MayProdList), junprodcount = len(JunProdList), julprodcount = len(JulProdList), augprodcount = len(AugProdList), sepprodcount = len(SepProdList), octprodcount = len(OctProdList), novprodcount = len(NovProdList), decprodcount = len(DecProdList),
                           JanTreatList = JanTreatList, FebTreatList = FebTreatList, MarTreatList = MarTreatList, AprTreatList = AprTreatList, MayTreatList = MayTreatList, JunTreatList = JunTreatList, JulTreatList = JulTreatList, AugTreatList = AugTreatList, SepTreatList = SepTreatList, OctTreatList = OctTreatList, NovTreatList = NovTreatList, DecTreatList = DecTreatList,
                            jantreatcount = len(JanTreatList), febtreatcount = len(FebTreatList), martreatcount = len(MarTreatList), aprtreatcount = len(AprTreatList), maytreatcount = len(MayTreatList), juntreatcount = len(JunTreatList), jultreatcount = len(JulTreatList), augtreatcount = len(AugTreatList), septreatcount = len(SepTreatList), octtreatcount = len(OctTreatList), novtreatcount = len(NovTreatList), dectreatcount = len(DecTreatList))




labels = []
values = []
colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


#Stat-Gen
@ feedback.route('/StatGen')
def CatGen():
    bar_labels = labels
    bar_values = values
    db = shelve.open('feedstorage.db', 'r')
    countDict = db['Feedback']
    db.close()

    JanGenList = []
    FebGenList = []
    MarGenList = []
    AprGenList = []
    MayGenList = []
    JunGenList = []
    JulGenList = []
    AugGenList = []
    SepGenList = []
    OctGenList = []
    NovGenList = []
    DecGenList = []

    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')
        cat = str(count.get_category())

        if datesplit[1] == '01' and cat == 'G':
            JanGenList.append(count)
        elif datesplit[1] == '02' and cat == 'G':
            FebGenList.append(count)
        elif datesplit[1] == '03' and cat == 'G':
            MarGenList.append(count)
        elif datesplit[1] == '04' and cat == 'G':
            AprGenList.append(count)
        elif datesplit[1] == '05' and cat == 'G':
            MayGenList.append(count)
        elif datesplit[1] == '06' and cat == 'G':
            JunGenList.append(count)
        elif datesplit[1] == '07' and cat == 'G':
            JulGenList.append(count)
        elif datesplit[1] == '08' and cat == 'G':
            AugGenList.append(count)
        elif datesplit[1] == '09' and cat == 'G':
            SepGenList.append(count)
        elif datesplit[1] == '10' and cat == 'G':
            OctGenList.append(count)
        elif datesplit[1] == '11' and cat == 'G':
            NovGenList.append(count)
        elif datesplit[1] == '12' and cat == 'G':
            DecGenList.append(count)
    return render_template('StatGen.html', title = 'Feedback - Category(General)', max = 20, labels = bar_labels, values = bar_values, JanGenList = JanGenList, FebGenList = FebGenList, MarGenList = MarGenList, AprGenList = AprGenList, MayGenList = MayGenList, JunGenList = JunGenList, JulGenList = JulGenList, AugGenList = AugGenList, SepGenList = SepGenList, OctGenList = OctGenList, NovGenList = NovGenList, DecGenList = DecGenList,
                    jangencount = len(JanGenList), febgencount = len(FebGenList), margencount = len(MarGenList), aprgencount = len(AprGenList), maygencount = len(MayGenList), jungencount = len(JunGenList), julgencount = len(JulGenList), auggencount = len(AugGenList), sepgencount = len(SepGenList), octgencount = len(OctGenList), novgencount = len(NovGenList), decgencount = len(DecGenList))


#Stat-Prod
@ feedback.route('/StatProd')
def CatProd():
    bar_labels = labels
    bar_values = values
    db = shelve.open('feedstorage.db', 'r')
    countDict = db['Feedback']
    db.close()

    JanProdList = []
    FebProdList = []
    MarProdList = []
    AprProdList = []
    MayProdList = []
    JunProdList = []
    JulProdList = []
    AugProdList = []
    SepProdList = []
    OctProdList = []
    NovProdList = []
    DecProdList = []

    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')
        cat = str(count.get_category())

        if datesplit[1] == '01' and cat == 'P':
            JanProdList.append(count)
        elif datesplit[1] == '02' and cat == 'P':
            FebProdList.append(count)
        elif datesplit[1] == '03' and cat == 'P':
            MarProdList.append(count)
        elif datesplit[1] == '04' and cat == 'P':
            AprProdList.append(count)
        elif datesplit[1] == '05' and cat == 'P':
            MayProdList.append(count)
        elif datesplit[1] == '06' and cat == 'P':
            JunProdList.append(count)
        elif datesplit[1] == '07' and cat == 'P':
            JulProdList.append(count)
        elif datesplit[1] == '08' and cat == 'P':
            AugProdList.append(count)
        elif datesplit[1] == '09' and cat == 'P':
            SepProdList.append(count)
        elif datesplit[1] == '10' and cat == 'P':
            OctProdList.append(count)
        elif datesplit[1] == '11' and cat == 'P':
            NovProdList.append(count)
        elif datesplit[1] == '12' and cat == 'P':
            DecProdList.append(count)
    return render_template('StatProd.html', title = 'Feedback - Category(Products)', max = 20, labels = bar_labels, values = bar_values, JanProdList = JanProdList, FebProdList = FebProdList, MarProdList = MarProdList, AprProdList = AprProdList, MayProdList = MayProdList, JunProdList = JunProdList, JulProdList = JulProdList, AugProdList = AugProdList, SepProdList = SepProdList, OctProdList = OctProdList, NovProdList = NovProdList, DecProdList = DecProdList,
                    janprodcount = len(JanProdList), febprodcount = len(FebProdList), marprodcount = len(MarProdList), aprprodcount = len(AprProdList), mayprodcount = len(MayProdList), junprodcount = len(JunProdList), julprodcount = len(JulProdList), augprodcount = len(AugProdList), sepprodcount = len(SepProdList), octprodcount = len(OctProdList), novprodcount = len(NovProdList), decprodcount = len(DecProdList))



#Stat-Treat
@ feedback.route('/StatTreat')
def CatTreat():
    bar_labels = labels
    bar_values = values
    db = shelve.open('feedstorage.db', 'r')
    countDict = db['Feedback']
    db.close()

    JanTreatList = []
    FebTreatList = []
    MarTreatList = []
    AprTreatList = []
    MayTreatList = []
    JunTreatList = []
    JulTreatList = []
    AugTreatList = []
    SepTreatList = []
    OctTreatList = []
    NovTreatList = []
    DecTreatList = []

    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')
        cat = str(count.get_category())

        if datesplit[1] == '01' and cat == 'T':
            JanTreatList.append(count)
        elif datesplit[1] == '02' and cat == 'T':
            FebTreatList.append(count)
        elif datesplit[1] == '03' and cat == 'T':
            MarTreatList.append(count)
        elif datesplit[1] == '04' and cat == 'T':
            AprTreatList.append(count)
        elif datesplit[1] == '05' and cat == 'T':
            MayTreatList.append(count)
        elif datesplit[1] == '06' and cat == 'T':
            JunTreatList.append(count)
        elif datesplit[1] == '07' and cat == 'T':
            JulTreatList.append(count)
        elif datesplit[1] == '08' and cat == 'T':
            AugTreatList.append(count)
        elif datesplit[1] == '09' and cat == 'T':
            SepTreatList.append(count)
        elif datesplit[1] == '10' and cat == 'T':
            OctTreatList.append(count)
        elif datesplit[1] == '11' and cat == 'T':
            NovTreatList.append(count)
        elif datesplit[1] == '12' and cat == 'T':
            DecTreatList.append(count)
    return render_template('StatTreat.html', title = 'Feedback - Category(Treatment)', max = 20, labels = bar_labels, values = bar_values, JanTreatList = JanTreatList, FebTreatList = FebTreatList, MarTreatList = MarTreatList, AprTreatList = AprTreatList, MayTreatList = MayTreatList, JunTreatList = JunTreatList, JulTreatList = JulTreatList, AugTreatList = AugTreatList, SepTreatList = SepTreatList, OctTreatList = OctTreatList, NovTreatList = NovTreatList, DecTreatList = DecTreatList,
                    jantreatcount = len(JanTreatList), febtreatcount = len(FebTreatList), martreatcount = len(MarTreatList), aprtreatcount = len(AprTreatList), maytreatcount = len(MayTreatList), juntreatcount = len(JunTreatList), jultreatcount = len(JulTreatList), augtreatcount = len(AugTreatList), septreatcount = len(SepTreatList), octtreatcount = len(OctTreatList), novtreatcount = len(NovTreatList), dectreatcount = len(DecTreatList))


@ feedback.route('/deleteFeedback/<uuid:id>', methods=['POST'])
def deleteFeedback(id):
    usersDict = {}
    db = shelve.open('feedstorage.db', 'w')
    usersDict = db['Feedback']
    usersDict.pop(id)
    db['Feedback'] = usersDict
    db.close()

    return redirect(url_for('feedback.retrieveFeedback'))