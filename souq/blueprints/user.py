from flask import Flask,Blueprint, render_template, request, redirect, session, flash, url_for
from souq.models import User, Card, TextItem,Item
# from souq.models import TextUser
from souq.forms import *
from flask_hashing import Hashing
from werkzeug.utils import *
import os


app = Flask(__name__)
hashing = Hashing(app)
app.config['media_path'] = '/media/suhaib/Suhaib/test/souq/static'
# define our blueprint
user_bp = Blueprint('user', __name__)
@user_bp.route('/registration', methods=['GET', 'POST'])
def register():
    # create instance of our form
    register = Registerion()
    # handle form submission
    if register.validate_on_submit():
        # create user object
        user = User()
        # set object attributes and create new user in database
        if register.image.data:
            image = register.image.data
            filename = secure_filename( register.username.data+image.filename )
            path = image.save(os.path.join(
            app.config['media_path'], 'photos', filename))
            print(path)
            user.profile_image = filename
        user.username = register.username.data
        user.email = register.email.data
        user.birthday = register.birthday.data
        user.password = hashing.hash_value(register.password.data, salt='abcd')
        user.first_name = register.first_name.data
        user.last_name = register.last_name.data
        user.biography = register.biography.data
        # save the user object
        user.save()
        flash('Thank you to join to our community.')
        return redirect(url_for('item.index'))
    else:
        return render_template("user/register.html", form=register,message= "here")

        # # another way
        # my_user = User(username = 'cookie', password = '1234')
        # my_user.save()

    # render the template
   


@user_bp.route('/user/edit/<id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.objects(id=id).first()
    # create instance of our form
    edit_user_form = EditUserForm()
    if request.method == "GET":
        edit_user_form.first_name.data = user.first_name
        edit_user_form.last_name.data = user.last_name
        edit_user_form.biography.data = user.biography
        edit_user_form.birthday.data = user.birthday
    # handle form submission
    if edit_user_form.validate_on_submit():
        data = edit_user_form.image.data
        if data is not None:
            image = edit_user_form.image.data
            filename = secure_filename( edit_user_form.username.data+image.filename )
            path = image.save(os.path.join(
            app.config['media_path'], 'photos', filename))
            print(path)
            user.profile_image = filename
        # read post values from the form
        first_name = edit_user_form.first_name.data
        last_name = edit_user_form.last_name.data
        biography = edit_user_form.biography.data
        # Update our user data
        user.first_name=first_name
        user.last_name=last_name
        user.biography=biography
        # save our changes to the DB
        user.save()
         # render the template
        return redirect(url_for('user.view_user' , id=session['user']['id']))


    # render the login template
    return render_template("user/edit.html", form=edit_user_form,user=user)



@user_bp.route('/profile/<id>')
def view_user(id):

    # get user by id
    user = User.objects(id=id).first()
    # render 'profile.html' blueprint with user
    items = TextItem.objects[:6].order_by('-created_at')
    print(items)
    return render_template('user/view.html', user=user , items = items)


@user_bp.route('/user/delete/<id>')
def delete_user(id):

    # get user by id
    User.objects(id=id).first().delete()
    session.clear()

    # render 'profile.html' blueprint with user
    return redirect(url_for('login.logout'))

@user_bp.route('/my-card')
def card():

    # get user favorite items 
    my_card = Card.objects(user=session['user']['id'], status= "False")
    # render 'card.html' blueprint with user
    return render_template('user/card.html', my_card = my_card)


@user_bp.route('/user/change_password', methods=['GET', 'POST'])
def change_password():
    user = User.objects(id=session['user']['id']).first()

    change_password_form = ChangePasswordForm()

    if change_password_form.validate_on_submit():
        # read post values from the form
        current_password = hashing.hash_value(change_password_form.current_password.data, salt='abcd')
        # new_password = change_password_form.new_password.data
        new_password = hashing.hash_value(change_password_form.new_password.data, salt='abcd')

        if (user.change_password(current_password, new_password)):
            user.save()
            flash("Your password has been successfully changed.")
            return redirect(url_for('user.change_password'))
        else:
            flash("Sorry the current password is wrong.")
    


    return render_template("user/changepassword.html", form=change_password_form)