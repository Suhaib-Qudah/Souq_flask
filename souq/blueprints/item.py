
from flask.helpers import flash
from itertools import *
from flask import Blueprint, render_template, request, session, redirect, url_for
import datetime
from souq.models import *
from souq.forms import *
from werkzeug.utils import *
import os
from mongoengine.queryset.visitor import Q


# define our blueprint
item_bp = Blueprint('item', __name__)
app = Flask(__name__)
app.config['media_path'] = '/media/suhaib/Suhaib/test/souq/static'


@item_bp.route('/', methods=['post','get'])
@item_bp.route('/items', methods=['post','get'])
def index():
    form = CategoryFilters()
    categories = Category.objects( status = 'active' )
    choices = []
    for category in categories:       
        choices.append(category.name)
    form.categories.choices = choices
    #to do when user try to filter by category 
    if request.method == "POST" and form.validate:
            items = Item.objects( category = form.categories.data).order_by('-created_at')
            message= (f'{items.count()} items were found in our store')
            flash(message)
            return render_template('item/items.html', items=items, title='Latest items',form=form)

    # get all items
    items = TextItem.objects().order_by('-created_at')
    # render 'souq' blueprint with items
    return render_template('item/items.html', items=items, title='Leatest items',form=form)


@item_bp.route('/item/add', methods=['GET', 'POST'])
def add_item():
    # create instance of our form
    new_item = AddItemForm()
    categories = Category.objects( status = 'active' )
    choices = []
    for category in categories:       
        choices.append(category.name)
    new_item.categories.choices = choices
    # handle form submission
    if new_item.validate_on_submit():
        # create instance of Textitem
        item = TextItem(store_name = session['user']['id'])
        if new_item.image.data:
            image = new_item.image.data
            print(image)
            filename = secure_filename( session['user']['username']+new_item.title.data+image.filename )
            path = image.save(os.path.join(
            app.config['media_path'], 'images', filename))
            print(path)
            item.image = filename
        # read item values from the form

        item.title = new_item.title.data
        item.content = new_item.body.data
        item.price = new_item.price.data
        item.quantity = new_item.quantity.data
        item.selling_price = new_item.selling_price.data
        item.category= new_item.categories.data
        item.tags = ["flask", "python", "mongo"]
        item.save()

        # render the template
        return redirect(url_for('item.index'))

    # render the template
    return render_template("item/add.html", form=new_item)


@item_bp.route('/item/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):

    # Find our item
    item = TextItem.objects(id=item_id).first()

    # create instance of our form
    edit_item_form = EdititemForm()

    if request.method == 'GET':
        edit_item_form.title.data = item.title
        edit_item_form.content.data = item.content

    # handle form submission
    if edit_item_form.validate_on_submit():

        # read item values from the form
        title = edit_item_form.title.data
        content = edit_item_form.content.data

        # Update our item title and content
        item.title = title
        item.content = content

        # save our changes to the DB
        item.save()

        # render the template
        return redirect(url_for('item.index'))

    # render the template
    return render_template("item/edit.html", form=edit_item_form)


@item_bp.route('/item/<item_id>',methods=['POST','GET'])
def view_item(item_id):
    item = TextItem.objects(id=item_id).first()
    # create instance of our form
    add_comment_form = AddCommentForm()
    # handle form submission
    if add_comment_form.validate_on_submit():
        # read item values from the form
        title = add_comment_form.title.data
        body = add_comment_form.body.data
        user = session['user']['id']
        # create instance of Textitem
        comment = Comment(content=body,author=user)
        # add comment to item comments
        item.comments.append(comment)
        item.save()
        
        return render_template('item/view.html', item=item ,form=add_comment_form)
        
    # get item

    # render the view
    return render_template('item/view.html', item=item,form=add_comment_form)


@item_bp.route('/item/delete/<item_id>')
def delete_item(item_id):

    # get item
    TextItem.objects(id=item_id).first().delete()

    # render the view
    return redirect(url_for('item.index'))

@item_bp.route('/deletecomment/<item_id>/<content>')
def delete_comment(item_id,content):
    # get item
    item = Item.objects(id=item_id).first()
    #get a comment of item
    item.comments
    count=0
    for i in item.comments:
        if i.content == content:
            item.comments.pop(count)
            item.save()
            break
        count+=1    
    # render the view
    return redirect(url_for('item.index'))



@item_bp.route('/additem/<item_id>' , methods=['GET', 'POST'] )
def add_item_to_card(item_id):
        item = Item.objects(id = item_id).first()
        card = Card(user = session['user']['id'],item_id = str(item.id),item_name = item.title,store_name=str(item.store_name.id))
        card.save()
        #Flash massage to let user now that item added
        flash("Item Added successfully to your card")
        # Redirect to home page 
        return redirect(url_for('item.index'))

@item_bp.route('/buy' , methods=['GET', 'POST'] )
def buy():
    if session:
                my_card = Card.objects(user=session['user']['id'], status= "False")
                for card_item in my_card: 
                    card_item.status = "Pending"
                      # Get item in item collection to check the card
                    card_item.save()
                    notification = Notification(
                    notification = (f"{card_item.user.username} want to buy {card_item.item_name}, please make sure you accept or denied the transaction."),
                    to = str(card_item.store_name)
                         )
                    notification.save()

        
                return render_template('user/thanks.html')
    else:
         flash("Sorry,  you don't authorize to do this action :'( ")
         return redirect(url_for('item.index'))
    

@item_bp.route('/pending')
def pending():
    items = Card.objects().filter(Q(status='Pending') & Q(store_name = str(session['user']['id'])))
    return render_template('dashboard/pending.html',items= items)

@item_bp.route('/card/delete-item/<card_item_id>')
def delete_item_from_card(card_item_id):

    # get item
    Card.objects(id=card_item_id).first().delete()
    flash("Item removed successfully from your card")
    # render the view
    return redirect(url_for('user.card'))


@item_bp.route('/card/accept-item/<id>')
def accept_item(id):
    card = Card.objects(id = id).first()
    card.status = 'Accept'
    card.save() 
    item = Item.objects(id = card.item_id).first()
    item.quantity -=1
    item.save()
    notification = Notification(
        notification = (f"{item.store_name.username} accepted your order, they will contact you soon"),
        to = str(card.user.id)
    )
    notification.save()
    flash("Item Accepted successfully ")
    # render the view
    return redirect(url_for('item.pending'))
