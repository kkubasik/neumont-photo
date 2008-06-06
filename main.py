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
            #print self.request.body
            #print user
           
        
           # upfile =  webapp.cgi.parse(fp=self.request.body_file)
            #(self.request.body_file, self.request.headers['CONTENT_TYPE'])
            #-------------------------------------- , pdict) (self.request.body)
            logging.log(logging.WARN, self.request.POST.items())
            p = Photo()
            p.title = self.request.get('Filename')
            p.author = user
            p.data = gzip.zlib.compress(self.request.body)
            #p.data = 
            p.put()
            
            
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
    def get(self, id):
        logging.log(logging.INFO, id)
     
        p = Photo.all().fetch(2)
        self.response.out.write(gzip.zlib.decompress(p[0].data))
        


def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/register', Register),
                                          ('/upload', UploadFiles),
                                          ('/uploaddata', UploadData),
                                          ('/view', ViewPhotos),
                                          ('/photo/(\d*)', PhotoSee)],
                                         debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
