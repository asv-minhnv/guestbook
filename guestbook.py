import cgi
import  os
import urllib
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
		#self.response.write('<html><body>')
		guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
		greeting_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)

		greetings = greeting_query.fetch(10)

		user= users.get_current_user();
		# for greeting in greetings:
		# 	if greeting.author:
		# 		author= greeting.author.email
		# 		if(user and user.user_id()) ==greeting.author.identity:
		# 			author+=' (You) '
		# 		self.response.write('<b>%s </b> wrote:' % author)
		# 	else:
		# 		self.response.write('An anonymous person wrote:')
		# 	self.response.write('<blockquote>%s</blockquote>' % cgi.escape(greeting.content))
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext= 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext='Login'
		template_values = {
			'user':user,
			'greetings':greetings,
			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
		}

		template = JINJA_EVIROMENT.get_template('index.html')
		self.response.write(template.render(template_values))
		# sign_query_params = urllib.urlencode({'guestbook_name': guestbook_name})
		# self.response.write(MAIN_PAGE_FOOTER_TEMPLATE % (sign_query_params, cgi.escape(guestbook_name),url,url_linktext))

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