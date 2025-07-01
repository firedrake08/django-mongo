from mongoengine import Document, StringField, IntField

class Lead(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    age = IntField()
    phone = StringField(required=True)
    meta = {
        'collection': 'leads'
    }
