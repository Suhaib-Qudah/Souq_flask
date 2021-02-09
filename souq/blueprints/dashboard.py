from itertools import count
from flask import Blueprint, render_template, session, redirect, url_for,flash
from souq.forms import AddCategory
from souq.models import *
from mongoengine.queryset.visitor import Q

# define our blueprint
dashboard_bp = Blueprint('dashboard', __name__)


# This is the home page of my dashboard
@dashboard_bp.route('/dashboard')
def home():
    # check if session is set to avoid errors
    if session.get('user'):
        if  session['user']['status'] == 'seller' or session['user']['status'] == 'admin' :
    # render 'dashboard' blueprint with items
            number_of_users = User.objects.count()
            number_of_user_items = Item.objects(store_name = session['user']['id']).count()
            number_of_user_notification = Notification.objects(seen=False,to = str(session['user']['id']) ).count()
            pendings = Card.objects(store_name = str(session['user']['id']),status='Pending').count()
            return render_template('dashboard/home.html', users=number_of_users , items = number_of_user_items, messages = number_of_user_notification,pendings=pendings)
        else:
             return redirect(url_for('item.index'))
    else: 
        return redirect(url_for('item.index'))


# Add category for the admin only
@dashboard_bp.route('/categories',methods=['GET', 'POST'])
def categories():
    # to be sure that he is the admin of the site 

    if session['user']['status'] == 'admin':
        form = AddCategory()
        if form.validate_on_submit():

            # read category values from the form
            name = form.name.data
            description = form.description.data
            status = form.status.data
            # To check that category name is unique
            if Category.get_by_name(Category, name):
                flash('Sorry this category is already in the system')
            else:
                new_category = Category(name=name, description=description, status=status)
                # add category to item comments
                new_category.save()
                flash('New Categories Added Successfully')
                return redirect(url_for('dashboard.categories'))

    # render 'dashboard' blueprint with items
        return render_template('dashboard/add_categories.html', form= form)
    else: 
        items = TextItem.objects()
        return render_template('item/items.html', items=items)


@dashboard_bp.route('/dashboard/users')
def users():

   if session:
       if session.get("user") and session['user']['status'] == 'admin' :
            # get all users
                users = User.objects()
                # render 'list.html' blueprint with users
                return render_template('user/list.html', users=users)
       else:
            flash("Sorry, You are not authorize to go to this page")
            return redirect(url_for('item.index'))
   else:
            flash("Sorry, You are not authorize to go to this page")
            return redirect(url_for('item.index'))



@dashboard_bp.route('/makeseller/<id>',methods=['GET'])
def create_seller(id):
    if session:
           if session['user']['status'] == 'admin':
                user = User.objects(id=id).first()
                user.status = 'seller'
                user.save()
                flash(f"{user.username} is now seller.")
                return redirect(url_for('dashboard.home'))


@dashboard_bp.route('/user/delete/<id>')
def delete_user(id):

    # get user by id
    user = User.objects(id=id).first()
    flash(f"{user.username} is deleted successfully")
    user.delete()
    return redirect(url_for('dashboard.home'))

    # render 'profile.html' blueprint with user

@dashboard_bp.route('/dashboard/your-items/')
def view_my_items():
    # get items of the user
    items = Item.objects(store_name=session['user']['id'])
    flash(f"This is Your Items")
    return render_template('dashboard/items.html', items = items)