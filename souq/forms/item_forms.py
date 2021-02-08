from souq.blueprints.dashboard import categories
from flask_wtf import *
from wtforms import *
from wtforms.validators import *


class AddItemForm(FlaskForm):
    title = StringField("Product name: ",validators=[ Length(min=10, max=20,message='at least 10 character for the title')],id='title')
    body = TextAreaField("Description: ",validators=[Length(200,30000,'the body of Item have to be at least 200 character')],default='Enter your product description')
    price = FloatField("Enter the price: ", validators=[DataRequired()])
    quantity = IntegerField("Enter the quantity: ", validators=[DataRequired()])
    selling_price = FloatField("Enter the selling price: ",validators=[DataRequired()])
    image = FileField("Browse for an image")
    categories = SelectField("Status: ", validators=[DataRequired()])
    submit = SubmitField("Add Item")


class EditItemForm(FlaskForm):
    title = StringField("Product name: ",validators=[ Length(min=10, max=20,message='at least 10 character for the title')],id='title')
    body = TextAreaField("Description: ",validators=[Length(200,30000,'the body of Item have to be at least 200 character')],default='Enter your product description')
    price = FloatField("Enter the price: ", validators=[DataRequired()])
    quantity = IntegerField("Enter the quantity: ", validators=[DataRequired()])
    selling_price = FloatField("Enter the selling price: ",validators=[DataRequired()])
    image = FileField("Browse for an image")
    categories = SelectField("Status: ", validators=[DataRequired()])
    submit = SubmitField("Add Item")

class AddCommentForm(FlaskForm):
    title = StringField("Enter a title: ")
    body = TextAreaField("Enter your Product Description: ")
    submit = SubmitField("Add comment: ")


class AddCard(FlaskForm):
    user_id = StringField()
    items = StringField()
