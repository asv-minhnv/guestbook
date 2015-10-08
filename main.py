import cgi
import logging
import  os
import urllib
import cStringIO
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import memcache
import webapp2
import jinja2


JINJA_EVIROMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

MAIN_PAGE_FOOTER_TEMPLATE= """\
    <form action ="/sign?%s" method="post">
        <div> <textarea name="content" rows="3" cols="60"></textarea></div>
         <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    <form> Guestbook name:
        <input value ="%s" name="guestbook_name">
        <input type ="submit" value = "swich">
    </form>
    <a href="%s">%s</a>
    </body>
    </html>
"""

DEFAULT_GUESTBOOK_NAME= 'default_guestbook'

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Comstructs an Datastore key for a Guestbook entity

    Web use guestbook_name as the key.
    """
    return ndb.Key('Guestbook',guestbook_name)

class Author(ndb.Model):
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

class Greeting(ndb.Model):
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        greetings = self.get_greetings(guestbook_name)
        stats = memcache.get_stats()

        self.response.write('<b>Cache Hits:{}</b><br>'.format(stats['hits']))
        self.response.write('<b>Cache Misses:{}</b><br><br>'.format(
                            stats['misses']))
        self.response.write(greetings)

        self.response.write("""
          <form action="/sign?{}" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
          <hr>
          <form>Guestbook name: <input value="{}" name="guestbook_name">
          <input type="submit" value="switch"></form>
        </body>
      </html>""".format(urllib.urlencode({'guestbook_name': guestbook_name}),
                        cgi.escape(guestbook_name)))

    def render_greetings(self, guestbook_name):

        greetings = ndb.gql('SELECT * FROM Greeting WHERE ANCESTOR IS :1 ORDER BY date DESC LIMIT 10', guestbook_key(guestbook_name))
       # greetings = ndb.gql('SELECT * FROM Greeting WHERE ANCESTOR IS :1 ORDER BY date DESC LIMIT 10',guestbook_key(guestbook_name))
        output = cStringIO.StringIO()
        for greeting in greetings:
            if greeting.author:
                output.write('<b>{}</b> wrote: '.format(greeting.author.email))
            else:
                output.write('An anonymous person wrote:')
            output.write('<blockquote>{}</blockquote>'.format(cgi.escape(greeting.content)))

        return output.getvalue()

    def get_greetings(sefl, guestbook_name):
        greetings = memcache.get('{}:greetings'.format(guestbook_name))
        if greetings is None:
            greetings = sefl.render_greetings(guestbook_name)
            if not memcache.add('{}:greetings'.format(guestbook_name),greetings,10):
                logging.error('Memcache set failed')
        return greetings

class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent = guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = Author(
                identity = users.get_current_user().user_id(),
                email =users.get_current_user().email()
            )
        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name':guestbook_name}
        self.redirect('/?'+urllib.urlencode((query_params)))

app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/sign', Guestbook)
], debug=True)