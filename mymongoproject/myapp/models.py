from mongoengine import Document, StringField, IntField, ReferenceField, DateTimeField
import datetime
from mongoengine.django.auth import User as MongoEngineUser

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

class User(MongoEngineUser):
    meta = {
        'collection': 'users'
    }

