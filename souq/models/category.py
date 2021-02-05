from mongoengine import *
from mongoengine.fields import *
from datetime import datetime


class Category(Document):
    #define class metadata
    meta = {'collection': 'category'}
    #define class fields

    #category name
    name = StringField(required=True,unique=True)
    #category description
    description = StringField()
    #category status (active or inactive)
    status = StringField(default='active')
    #the date that admin add the category to the site 
    add_at = DateTimeField(default=datetime.utcnow)

    def get_by_name(cls, name):
        data = Category.objects.get(name = name)
        if data is not None:
            return True
        else:
            return False


