from google.appengine.ext import db
from google.appengine.ext import blobstore

class Sermon(db.Model):
	blob_key = blobstore.BlobReferenceProperty(required=True)
	tags = db.StringProperty() #db.ListProperty(db.Category)
	date = db.DateProperty()
	isAM = db.BooleanProperty()
	title = db.StringProperty()
	series = db.StringProperty()
	book = db.StringProperty()
	begin_chapter = db.IntegerProperty()
	end_chapter = db.IntegerProperty()
	begin_verse = db.IntegerProperty()
	end_verse = db.IntegerProperty()
	summary = db.StringProperty()
	preacher = db.StringProperty()