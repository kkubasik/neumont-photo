import os 
from google.appengine.ext import webapp, db
from google.appengine.api import users
from google.appengine.ext.webapp import template



class Photo(db.Model):
  author = db.UserProperty()
  title = db.StringProperty()
  data = db.BlobProperty()
  uploaded = db.DateTimeProperty()
  
class Profile(db.Model):
  user = db.UserProperty()
  neumont_mail = db.EmailProperty()
  verify_value = db.StringProperty()
  valid = db.BooleanProperty()
  