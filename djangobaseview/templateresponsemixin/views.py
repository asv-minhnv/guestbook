import urllib

from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from google.appengine.api import users

from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME

class IndexView(ListView):

	guestbook_name = DEFAULT_GUESTBOOK_NAME

	greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
	greetings = greetings_query.fetch(10)

	if users.get_current_user():
		url = users.create_logout_url('/')
		url_linktext = 'Logout'
	else:
		url = users.create_login_url('/')
		url_linktext = 'Login'

	template_values = {
		'greetings': greetings,
		'guestbook_name': guestbook_name,
		'url': url,
		'url_linktext': url_linktext,
	}
	queryset= template_values
	context_object_name= "greetings"
	template_name= "templateresponsemixin/main_page.html"

class SignView(TemplateView):
	def post(self,request):
		guestbook_name = request.POST.get('guestbook_name')
		greeting = Greeting(parent=guestbook_key(guestbook_name))
		if users.get_current_user():
			greeting.author = users.get_current_user()

		greeting.content = request.POST.get('content')
		greeting.put()
		return HttpResponseRedirect('/templateresponsemixin/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
