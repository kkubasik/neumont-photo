#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import wsgiref.handlers

import os 
from google.appengine.ext import webapp, db
from google.appengine.api import users
from google.appengine.ext.webapp import template
from datadef import *
from google.appengine.ext.admin import  logging


class MainHandler(webapp.RequestHandler):
  import sys

  def get(self):
    user = users.get_current_user()
    if user:
      self.response.out.write('Hello %s!' % user.nickname)
    else:
      self.redirect(users.create_login_url(self.request.uri))

class Register(webapp.RequestHandler):
  
  def get(self):
    
    user = users.get_current_user()
    
    if user:
      profile = Profile.gql("WHERE user = :1", users.get_current_user())
      template_values = {
        'user': users.get_current_user(),
        'logout_url': users.create_logout_url(self.request.uri),
        'profile': profile,
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/registration.html')
      self.response.out.write(template.render(path, template_values))
    else:
      self.redirect(users.create_login_url(self.request.uri))
  def post(self):
    self.response.out.write("POST") 


class UploadFiles(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    
    if user:
       profile = Profile.gql("WHERE user = :1", users.get_current_user())
       template_values = {
        'user': users.get_current_user(),
    'logout_url': users.create_logout_url(self.request.uri),
    'profile': profile,
      }
       path = os.path.join(os.path.dirname(__file__), 'templates/upload.django.html')
       self.response.out.write(template.render(path, None))
    else:
      self.redirect(users.create_login_url(self.request.uri))


class UploadData(webapp.RequestHandler):

  def post(self):
    
    user = users.get_current_user()
    
    if user:
       upfile = self.request.body()
       logging.log(logging.INFO, self.request)
       path = os.path.join(os.path.dirname(__file__), 'templates/upload.django.html')
       self.response.out.write(template.render(path, None))
    else:
      self.redirect(users.create_login_url(self.request.uri))
  
  
def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/register', Register),
                                        ('/upload', UploadFiles),
                                        ('/uploaddata', UploadData)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
