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
import gzip
import datetime
from getimageinfo import getImageInfo

class MainHandler(webapp.RequestHandler):
    import sys

    def get(self):
        '''
      Get Main Index
      '''
        user = users.get_current_user()
        if user:
            self.response.out.write('Hello %s!' % user.nickname)
            p = Profile.gql("WHERE user = :1", users.get_current_user())
            if p.count() < 1:
                newp = Profile()
                newp.user = user
                newp.valid = False
                newp.put()
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
            profile = Profile.gql("WHERE user = :1", user)
            template_values = {
                'user': user,
                'logout_url': users.create_logout_url(self.request.uri),
                'profile': profile.fetch(1),
                'url': self.request.host_url,
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/upload.django.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))


class UploadData(webapp.RequestHandler):

    def post(self):
        '''
      Save the files submitted as a new photo, get metadata from throughout POST
      '''
        user = users.get_current_user()
        
        if user:
            c =0
            while self.request.POST.get('defaults_%i'%c) is not None:
                p = Photo()
                try:
                    
                    p.title = self.request.POST.get('defaults_%i'%c).filename
                   
                    p.author = user
                    p.data = gzip.zlib.compress(self.request.POST.get('defaults_%i'%c).file.read())
                    p.put()
                except:
                    logging.log(logging.ERROR, "Bad File Upload")
                c= c+1
            
            
            #path = os.path.join(os.path.dirname(__file__), 'templates/upload.django.html')
            #self.response.out.write(template.render(path, None))
        else:
            logging.log(logging.ERROR,'not logged in!')
            logging.log(logging.ERROR, self.request.get('Cookie'))
            self.redirect(users.create_login_url(self.request.uri))

class ViewPhotos(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            profile = Profile.gql("WHERE user = :1", users.get_current_user())
            template_values = {
                'user': users.get_current_user(),
                'logout_url': users.create_logout_url(self.request.uri),
                'profile': profile.fetch(1),
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/display.django.html')
            self.response.out.write(template.render(path, None))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
            
class PhotoSee(webapp.RequestHandler):
    def get(self, key):
        im = db.get(db.Key(key))
        if not im:
            self.error(404)
            return
        
        content_type, width, height = getImageInfo(im.content)
        self.response.headers.add_header("Expires", datetime.datetime.today())
        self.response.headers["Content-Type"] = content_type
        self.response.out.write(im.content)
        


def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/register', Register),
                                          ('/upload', UploadFiles),
                                          ('/uploaddata', UploadData),
                                          ('/view', ViewPhotos),
                                          ('/photo/(.*)', PhotoSee)],
                                         debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
