#!/usr/bin/env python
# (c) 2010 Mr David S. Hollands BSc Lond

import os
import datetime

import gdata.service
import gdata.alt.appengine
import gdata.calendar
import gdata.calendar.service

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext import blobstore

class Sermon(db.Model):
	blob = blobstore.BlobReferenceProperty()
	

class Event:
	def __init__(self, title):
		self.title = title
		
	def setWhere(self, where):
		self.where = where
	
	def setStart(self, s_date_time):
		self.start = s_date_time
		self.start_string = s_date_time.ctime()[0:16]

	def setEnd(self, e_date_time):
		self.end = e_date_time
		self.end_string = e_date_time.ctime()[0:16]
		
	def __repr__(self):
		return repr((self.title, self.where, self.start, self.end))


# http://hwec.org.uk
class MainHandler(webapp.RequestHandler):
	def __init__(self):
		# Initialize a client to talk to Google Data API services.
		self.cal_client = gdata.calendar.service.CalendarService()
		gdata.alt.appengine.run_on_appengine(self.cal_client)
	
	def get(self):
		try:	
			# Get the events occuring this week.
			query = gdata.calendar.service.CalendarEventQuery(
				'gvv0r5bld0rh09um7j2d10e3gs@group.calendar.google.com', 
				'public', 'full')
			today = datetime.date.today()
			a_week_from_today = today + datetime.timedelta(7)
			query.start_min = today.isoformat()
			query.start_max = a_week_from_today.isoformat()
			feed = self.cal_client.CalendarQuery(query)
		
			# Read in and objectify event start and end times
			events = []
			for e in feed.entry:
				event = Event(e.title.text)
				for w in e.where:
					event.setWhere(w.value_string)
				for a in e.when:
					event.setStart(datetime.datetime.strptime(
						a.start_time[0:18], '%Y-%m-%dT%H:%M:%S'))
					event.setEnd(datetime.datetime.strptime(
						a.end_time[0:18], '%Y-%m-%dT%H:%M:%S'))	
				if event.start: 
					events.append(event)
				events.sort(key=lambda event: (event.start.month, event.start.day))
		except:
			pass	

		# Populate index.html template values (Django template).
		page_template_values = {
			'remote_addr': self.request.remote_addr,
			'events': events, #feed.entry,
			'year': datetime.date.today().year,
			}
					
		# Render template in response.	
		path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
		self.response.out.write(template.render(path, page_template_values))

class AboutHandler(webapp.RequestHandler):
	
	""" Populate base.html template values.
		 	Decide which content template to render.
		 	Render template in response."""
	def get(self):
		page_template_values = {
			'remote_addr': self.request.remote_addr,
			'year': datetime.date.today().year,
			'debug': self.request.path,
			}
		
		request_path = self.request.path
		if request_path == '/about/belonging/' or request_path == '/about/belonging':
			path = os.path.join(os.path.dirname(__file__), 'templates/about/belonging.html')
		elif request_path == '/about/location/' or request_path == '/about/location':
			path = os.path.join(os.path.dirname(__file__), 'templates/about/location.html')
		elif request_path == '/about/christianity/' or request_path == '/about/christianity':
			path = os.path.join(os.path.dirname(__file__), 'templates/about/nutshell.html')
		else:
			path = os.path.join(os.path.dirname(__file__), 'templates/about/base_about.html')
		
		self.response.out.write(template.render(path, page_template_values))											



class EventsHandler(webapp.RequestHandler):
	""" Populate base.html template values.
		 	Decide which content template to render.
		 	Render template in response."""
	def get(self):
		page_template_values = {
			'remote_addr': self.request.remote_addr,
			'year': datetime.date.today().year,
			'debug': self.request.path,
			}
			
		request_path = self.request.path
		if request_path == '/events/weekly/' or request_path == '/events/weekly':
			path = os.path.join(os.path.dirname(__file__), 'templates/events/base_events.html')
		elif request_path == '/events/monthly/' or request_path == '/events/monthly':
			path = os.path.join(os.path.dirname(__file__), 'templates/events/monthly.html')
		elif request_path == '/events/annual/' or request_path == '/events/annual':
			path = os.path.join(os.path.dirname(__file__), 'templates/events/annual.html')
		else:
			path = os.path.join(os.path.dirname(__file__), 'templates/events/base_events.html')
		
		self.response.out.write(template.render(path, page_template_values))


class AudioHandler(webapp.RequestHandler):
	""" Populate base.html template values.
		 	Decide which content template to render.
		 	Render template in response."""
	def get(self):
		page_template_values = {
			'remote_addr': self.request.remote_addr,
			'year': datetime.date.today().year,
			'debug': self.request.path,
			}


class ArticleHandler(webapp.RequestHandler):
	""" Populate base.html template values.
		 	Decide which content template to render.
		 	Render template in response."""
	def get(self):
		page_template_values = {
			'remote_addr': self.request.remote_addr,
			'year': datetime.date.today().year,
			'debug': self.request.path,
			}


class ContactHandler(webapp.RequestHandler):
	""" Populate base.html template values.
		 	Decide which content template to render.
		 	Render template in response."""
	def get(self):
		page_template_values = {
			'remote_addr': self.request.remote_addr,
			'year': datetime.date.today().year,
			'debug': self.request.path,
			}



def main():
	application = webapp.WSGIApplication(
			[('/', MainHandler),
			('/about/.*', AboutHandler),
			('/events/.*', EventsHandler),
			('/audio/.*', AudioHandler),
			('/articles/.*', ArticleHandler),
			('/contact/.*', ContactHandler),
			], debug=True)																
	util.run_wsgi_app(application)
		
if __name__ == '__main__':
	main()
