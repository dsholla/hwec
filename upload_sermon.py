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


class Sermon(db.Model):
	blob = blobstore.BlobReferenceProperty(required=True)
#	tags = db.StringProperty() #db.ListProperty(db.Category)
#	date = db.DateProperty()
#	isAM = db.BooleanProperty()
#	title = db.StringProperty()
#	series = db.StringProperty()
#	book = db.StringProperty()
#	begin_chapter = db.IntegerProperty()
#	end_chapter = db.IntegerProperty()
#	begin_verse = db.IntegerProperty()
#	end_verse = db.IntegerProperty()
#	summary = db.StringProperty()
#	preacher = db.StringProperty()

class MainHandler(webapp.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/upload')

		# Populate index.html template values (Django template).
		page_template_values = {
			'remote_addr': self.request.remote_addr,
			'upload_url': upload_url
			}

		# Render template in response.	
		path = os.path.join(os.path.dirname(__file__), 'templates/upload_sermon.html')
		self.response.out.write(template.render(path, page_template_values))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		# 'file' is file upload field in the form
		upload_files = self.get_uploads('file')  
		blob_info = upload_files[0]
		
		if self.request.get("rad_isAM") == "Yes":
			isAM = True
		else:
			isAM = False
		
		sermon = Sermon(blob=blob_info.key())
#		sermon.tags = self.request.get('txt_tags')
#		sermon.date = datetime.date.strptime(self.request.get('date'), '%Y-%m-%d')
#		sermon.isAM = isAM
#		sermon.title = self.request.get('txt_title')
#		sermon.series = self.request.get('txt_series')
#		sermon.book = self.request.get('sel_book')
#		sermon.begin_chapter = self.request.get('begin_chapter')
#		sermon.end_chapter = self.request.get('end_chapter')
#		sermon.begin_verse = self.request.get('begin_verse')
#		sermon.end_verse = self.request.get('end_verse')
#		sermon.summary = self.request.get('txt_summary')
#		sermon.preacher = self.request.get('txt_preacher')
		
		db.put(sermon)
		
		self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

def main():
	application = webapp.WSGIApplication(
					[('/upload_sermon', MainHandler),
 					('/upload', UploadHandler),
					('/serve/([^/]+)?', ServeHandler), #
					], debug=True)
	run_wsgi_app(application)

if __name__ == '__main__':
	main()