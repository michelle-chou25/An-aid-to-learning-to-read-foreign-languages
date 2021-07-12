from django.db import models
import mongoengine
#
# Create your models here.
# from django import models

class C2ecol(mongoengine.Document):
    traditional = mongoengine.StringField(max_length=255)
    simplified = mongoengine.StringField(max_length=500)
    pinyin = mongoengine.StringField(max_length=500)
    definitions = mongoengine.ListField()
