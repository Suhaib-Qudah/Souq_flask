from mongoengine import *
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import *
from wtforms.validators import Required
from .user import User
from datetime import datetime


class Card(Document):
    #define class metadata
    meta = {'collection': 'card', 'allow_inheritance': True}
    #define class fields
    user = ReferenceField( User , reverse_delete_rule=CASCADE )
    item_name = StringField()
    item_id = StringField()
    store_name = StringField(Required=True)
    add_at = DateTimeField(default=datetime.utcnow)
    status = StringField( default='False' )

