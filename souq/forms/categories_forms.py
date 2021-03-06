from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length


status_choices = [('active', 'Active'),('inactive','Inactive')]
class AddCategory(FlaskForm):
    name = StringField("Category Name: ",validators=[ Length(min=5, max=20,message='at least 10 character for the category name')],id='name')
    description = TextAreaField("Description: ")
    status = SelectField("Status: ", validators=[DataRequired()],choices=status_choices)
    submit = SubmitField("Add New Category")



class CategoryFilters(FlaskForm):
    categories = SelectField("Category Name: ")
    submit = SubmitField("Search Now")


