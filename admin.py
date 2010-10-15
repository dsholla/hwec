#!/usr/bin/env python
#

import os
import urllib
import datetime
import string

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Sermon

class SermonUploadFormHandler(webapp.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/admin/upload_sermon')
		page_template_values = {
			'remote_addr': self.request.remote_addr,
			'upload_url': upload_url
			}

		# Render template in response.	
		path = os.path.join(os.path.dirname(__file__), 'templates/upload_sermon.html')
		self.response.out.write(template.render(path, page_template_values))


class SermonUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		
		if self.request.get("rad_isAM") == "Yes":
			isAM = True
		else:
			isAM = False
			
		try:
			for upload in self.get_uploads():
				sermon = Sermon(blob_key=upload.key())
				db.put(sermon)
			
			self.redirect('/upload_success.html')

		except:
			self.redirect('/upload_failure.html')

def main():
	application = webapp.WSGIApplication(
		[('/admin/upload_sermon_form', SermonUploadFormHandler),
		('/admin/upload_sermon', SermonUploadHandler),
		], debug=True)																
	run_wsgi_app(application)
		
if __name__ == '__main__':
	main()