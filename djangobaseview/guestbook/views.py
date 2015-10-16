import urllib
from google.appengine.api import users
from google.appengine.api import memcache
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from guestbook.models import Greeting, Guestbook


class IndexView(TemplateView):
	template_name = "guestbook/index.html"

	def post(self, request, *args, **kwargs):
		guestbook_name = request.POST.get('guestbook_name')
		content = request.POST.get('content')
		Greeting.add_greeting(content, guestbook_name)
		return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		guestbook_name = self.request.GET.get('guestbook_name',Guestbook.get_default_guestbook())
		greetings = Greeting.get_latest(guestbook_name,10)
		if users.get_current_user():
			url = users.create_logout_url(self.request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linktext = 'Login'
		template_values = {
			'greetings': greetings,
			'guestbook_name': guestbook_name,
			'url': url,
			'url_linktext': url_linktext,
		}
		template_values.update(context)
		return template_values