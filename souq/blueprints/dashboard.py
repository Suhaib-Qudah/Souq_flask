from souq.models.category import Category
from flask.helpers import flash
from souq.blueprints.user import card
from souq.models.item import Item
from itertools import count
from flask import Blueprint, render_template, request, session, redirect, url_for
import datetime
from souq.models import User, comment, Card, user
from souq.models import Comment
from souq.forms import AddCategory


from souq.models import TextItem
from souq.forms import AddItemForm, EditItemForm , AddCommentForm

# define our blueprint
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
def home():
    # get all items
    if session['user']['status'] == 'seller' or session['user']['status'] == 'admin' :
    # render 'dashboard' blueprint with items
        number_of_users = User.objects.count()
        number_of_user_items = Item.objects(store_name = session['user']['id']).count()
        return render_template('dashboard/home.html',users=number_of_users , items = number_of_user_items)
    else: 
        items = TextItem.objects()
        return render_template('item/items.html', items=items)


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
            if (Category.get_by_name(Category,name)):
                flash('Sorry this category is already in the system')
            else:
                new_category = Category(name=name,description=description, status=status)
                # add category to item comments
                new_category.save()

    # render 'dashboard' blueprint with items
        return render_template('dashboard/add_categories.html', form= form)
    else: 
        items = TextItem.objects()
        return render_template('item/items.html', items=items)
