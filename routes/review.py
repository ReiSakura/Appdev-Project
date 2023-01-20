from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from data.Review import Review
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, TextAreaField, validators
import shelve
from .database import db
import os

review = Blueprint("review", __name__, static_folder=os.path.join(
    os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"))


class CreateReviewForm(FlaskForm):
        first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
        last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
        gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
    default='')
        rating = SelectField('Rating', [validators.DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'),('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')],
    default='5')
        remarks = TextAreaField('Remarks', [validators.Optional()])


class Review(db.Model): #how to do this part help
    id = db.Column



@ review.route('/', methods=['GET', 'POST'])
def get_review():
    '''
    Main page
    '''
    return render_template('review.html') #headings and all that required??


@ review.route('/add', methods=['GET', 'POST'])
def add_review():
    '''
    Add review page
    '''
    # Create the form.
    form = CreateReviewForm()

    #Validations
    if form.addSubmit.data and form.validate_on_submit():
        flash('Review added', 'success')
        return redirect('/review/')
    return render_template('addreview.html', form=form)


@ review.route('/<int:id>', methods=['POST'])
def delete_review(id):
    '''
    Delete data in review based on id
    '''
    if request.method == "POST":
        review = db.get_or_404(reviews, id)
        db.session.delete(review)
        db.session.commit()
        return redirect(url_for('review.get_review'))

    return "Failed to delete"

#     create_review_form = CreateReviewForm(request.form)
#     if request.method == 'POST' and create_review_form.validate():
#         reviews_dict = {}
#         db = shelve.open('review.db', 'c')

#         try:
#             reviews_dict = db['Review']
#         except:
#             print("Error in retrieving Reviews from review.db.")

#         review = User.User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.gender.data, create_user_form.membership.data, create_user_form.remarks.data)
#         users_dict[user.get_user_id()] = user
#         db['Users'] = us_dict

#         db.close()

#         return redirect(url_for('retrieve_users'))
#     return render_template('createUser.html', form=create_user_form)


# @ review.route('/retrieveUsers')
# def retrieve_users():
#     users_dict = {}
#     db = shelve.open('user.db', 'r')
#     users_dict = db['Users']
#     db.close()

#     users_list = []
#     for key in users_dict:
#         user = users_dict.get(key)
#         users_list.append(user)

#     return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)


# @ review.route('/retrieveCustomers')
# def retrieve_customers():
#     customers_dict = {}
#     db = shelve.open('customer.db', 'r')
#     customers_dict = db['Customers']
#     db.close()

#     customers_list = []
#     for key in customers_dict:
#         customer = customers_dict.get(key)
#         customers_list.append(customer)

#     return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)


# @ review.route('/edit/<int:id>/', methods=['GET', 'POST'])
# def edit(id):
#     update_user_form = CreateUserForm(request.form)
#     if request.method == 'POST' and update_user_form.validate():
#         users_dict = {}
#         db = shelve.open('user.db', 'w')
#         users_dict = db['Users']

#         user = users_dict.get(id)
#         user.set_first_name(update_user_form.first_name.data)
#         user.set_last_name(update_user_form.last_name.data)
#         user.set_gender(update_user_form.gender.data)
#         user.set_membership(update_user_form.membership.data)
#         user.set_remarks(update_user_form.remarks.data)

#         db['Users'] = users_dict
#         db.close()

#         return redirect(url_for('retrieve_users'))
#     else:
#         users_dict = {}
#         db = shelve.open('user.db', 'r')
#         users_dict = db['Users']
#         db.close()

#         user = users_dict.get(id)
#         update_user_form.first_name.data = user.get_first_name()
#         update_user_form.last_name.data = user.get_last_name()
#         update_user_form.gender.data = user.get_gender()
#         update_user_form.membership.data = user.get_membership()
#         update_user_form.remarks.data = user.get_remarks()

#         return render_template('updateUser.html', form=update_user_form)


