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

# standard imports you should have already been using
import webapp2
import logging
from webapp2_extras import jinja2
import urllib

# this library is for decoding json responses
from webapp2_extras import json

import numpy
# this is used for constructing URLs to google's APIS
from apiclient.discovery import build

# This uses discovery to create an object that can talk to the
# fusion tables API using the developer key
API_KEY = 'AIzaSyDhOSXPy4pEd1JozYgsVfrVWqrAvajhq24'
TABLE_ID = '1aGXNJqLTp2HtkXyMW0QJsQGVPvuiM9Ty7v5TkfDM'

service = build('fusiontables', 'v1', developerKey=API_KEY)
request = service.column().list(tableId=TABLE_ID)

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    # This will call self.response.write using the specified template and context.
    # The first argument should be a string naming the template file to be used.
    # The second argument should be a pointer to an array of context variables
    #  that can be used for substitutions within the template
    # lets jinja render our response
    def render_response(self, _template, context):
        values = {'url_for': self.uri_for}

        logging.info(context)
        values.update(context)
        self.response.headers['Content-Type'] = 'text/html'

        # Renders a template and writes the result to the response.
        try:
            rv = self.jinja2.render_template(_template, **values)
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write(rv)
        except TemplateNotFound:
            self.abort(404)

class MainHandler(BaseHandler):
    def get(self):
        logging.info("Hello")
        data = self.get_all_data()
        context = {}

        # and render the response
        self.render_response('index.html', context)


    # collect the data from google fusion tables
    # pass in the name of the file the data should be stored in
    def get_all_data(self):
        """ collect data from the server. """
        # limited to 10 rows
        query = "SELECT * FROM " + TABLE_ID + " WHERE  AnimalType = 'CAT' LIMIT 10"
        response = service.query().sql(sql=query).execute()
        logging.info(response)
        return response

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
