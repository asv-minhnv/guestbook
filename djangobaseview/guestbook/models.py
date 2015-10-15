import logging
from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    '''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    '''Models an individual Guestbook entry.'''
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def get_latest(guestbook_name, count):
    	greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    	greetings = greetings_query.fetch(count)
        return greetings

    @staticmethod
    def save_greeting(request,guestbook_name):
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = users.get_current_user()
        greeting.content = request.POST.get('content')
        greeting.put()
        Guestbook.save_guestbook(guestbook_name)


class Guestbook(ndb.Model):
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def get_list():
        guestbook = Guestbook()
        guestbook_query = guestbook.query(ancestor=guestbook_key()).order(-Guestbook.date)
        guestbook._result_cache = None
        guestbooks = guestbook_query.fetch()
        return guestbooks

    @staticmethod
    def get_guestbook_by_name(guestbook_name):
        guestbook = Guestbook.query(Guestbook.name==guestbook_name).get()
        return guestbook

    @staticmethod
    def save_guestbook(guestbook_name):
        check_guestbook = Guestbook.get_guestbook_by_name(guestbook_name)
        if check_guestbook is None:
            guestbook = Guestbook(parent=guestbook_key())
            guestbook.name= guestbook_name
            guestbook.put()


    # @staticmethod
    # def check_guestbook(guestbook_name):




