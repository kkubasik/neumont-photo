import os 
from google.appengine.ext import webapp, db
from google.appengine.api import users
from google.appengine.ext.webapp import template



class Photo(db.Model):  
    '''
    Photo Store!
    '''
    author = db.UserProperty()
    title = db.StringProperty()
    data = db.BlobProperty()
    uploaded = db.DateTimeProperty()
    tags = db.StringListProperty('tags_list')
  
class Profile(db.Model):
    '''
    Profile/Login/Validation information
    '''
    user = db.UserProperty()
    neumont_mail = db.EmailProperty()
    verify_value = db.StringProperty()
    verify_sent = db.DateTimeProperty()
    valid = db.BooleanProperty()
  