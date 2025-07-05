from mongoengine import Document, StringField, IntField, ReferenceField, DateTimeField
import datetime
from django.contrib.auth.hashers import make_password, check_password

class Lead(Document):
    STATUS_CHOICES = ["New", "Contacted", "Not interested", "Interested", "Later"]
    SOURCE_CHOICES = ["website form", "referral", "marketing campaign"]
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    age = IntField()
    phone = StringField(required=True)
    status = StringField(choices=STATUS_CHOICES, default="New")
    source = StringField(choices=SOURCE_CHOICES, required=True)
    meta = {
        'collection': 'leads'
    }

class Activity(Document):
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    lead = ReferenceField(Lead, required=True)
    
    meta = {
        'collection': 'activities'
    }


class User(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    meta = {
        'collection': 'users'
    }

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

