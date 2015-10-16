import logging
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
	def get_key_by_id(cls, guestbook_name, greeting_id):
		try:
			greeting_id = int(greeting_id)
		except ValueError:
			raise ValueError("Greeting ID must be a positive integer. Please try again!")

		return ndb.Key("Guestbook", str(guestbook_name), "Greeting", greeting_id)

	@classmethod
	def get_greeting(cls, guestbook_name, greeting_id):
		greeting_key=cls.get_key_by_id(guestbook_name, greeting_id)
		return cls.query(ancestor=greeting_key).order(-cls.date).get()

	@classmethod
	def delete(cls,guestbook_name, greeting_id):
		greeting_key=cls.get_key_by_id(guestbook_name, greeting_id)
		greeting_key.delete()


	@classmethod
	def add_greeting(cls, content, guestbook_name):
		greeting = cls(parent=cls.get_key_guesbook(guestbook_name))
		if users.get_current_user():
			greeting.author = users.get_current_user()
		greeting.content = content
		greeting.put()

	@classmethod
	def update_greeting(cls, content, guestbook_name, greeting_id):
		greeting_key=cls.get_key_by_id(guestbook_name, greeting_id)
		greeting = cls.query(ancestor=greeting_key).order(-cls.date).get()
		greeting.content = content
		greeting.put()
