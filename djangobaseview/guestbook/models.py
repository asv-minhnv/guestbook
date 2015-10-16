from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.



class Greeting(ndb.Model):
	'''Models an individual Guestbook entry.'''
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_default_guestbook(cls):
		return 'default_guestbook'

	@classmethod
	def get_key_guesbook(cls, guestbook_name):
		if not guestbook_name:
			guestbook_name = cls.get_default_guestbook()
		return ndb.Key('Guestbook', guestbook_name)

	@classmethod
	def get_latest(cls, guestbook_name, count):
		greetings_query = cls.query(ancestor=cls.get_key_guesbook(guestbook_name)).order(-cls.date)
		greetings = greetings_query.fetch(count)
		return greetings

	@classmethod
	def add_greeting(cls, content, guestbook_name):
		greeting = cls(parent=cls.get_key_guesbook(guestbook_name))
		if users.get_current_user():
			greeting.author = users.get_current_user()
		greeting.content = content
		greeting.put()
