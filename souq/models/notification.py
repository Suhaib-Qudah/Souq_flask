from mongoengine import *
from mongoengine.fields import *
from datetime import datetime


class Notification(Document):
    # define class metadata
    meta = {'collection': 'notification', 'allow_inheritance': True}
    # define class fields
    notification = StringField(max_length=300 , required=True)
    created_at = DateTimeField(default=datetime.now())
    to = StringField(required = True)
    seen = BooleanField(required = True,default=False)
    seen_at = DateTimeField()



    
    

