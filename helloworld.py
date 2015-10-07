import webapp2
from google.appengine.api import users



class MainPage (webapp2.RequestHandler):
	def get(self):
		#Check for active for accont session
		user = users.get_current_user()

		if user:
			# self.response.headers['Content-Type'] = 'text/html; charset=uft-8'
			# self.response.write('Hello, '+ user.nickname())
			greeting = ('Welcome, %s (<a href="%s"> Sign Out </a>)' % (user.nickname(), users.create_logout_url('/')))
		else:
			greeting = ('<a href="%s"> Sign in or register </a>' % (users.create_login_url('/')))
			#self.redirect(users.create_login_url(self.request.uri))
		self.response.out.write('<html><body>%s <body></html>' % greeting)
app = webapp2.WSGIApplication([
	('/',MainPage)
], debug=True)