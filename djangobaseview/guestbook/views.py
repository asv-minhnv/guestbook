import logging
import urllib
from google.appengine.api import users
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from guestbook.models import Greeting, Guestbook,  guestbook_key, DEFAULT_GUESTBOOK_NAME


class IndexView(TemplateView):
	template_name = "guestbook/index.html"

	def post(self, request, *args, **kwargs):
		guestbook_name = request.POST.get('guestbook_name')
		Guestbook.save_guestbook(guestbook_name)
		return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['guestbooks'] = Guestbook.get_list()
		return  context


class GuestbookView(TemplateView):
	template_name = "guestbook/guestbook.html"

	def post(self, request, *args, **kwargs):
		guestbook_name = request.POST.get('guestbook_name')
		Greeting.save_greeting(request, guestbook_name)
		return HttpResponseRedirect('/guestbook/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

	def get_context_data(self, **kwargs):
		context = super(GuestbookView, self).get_context_data(**kwargs)
		guestbook_name = self.request.GET.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
		greetings = Greeting.get_latest(guestbook_name,10)
		if users.get_current_user():
			url = users.create_logout_url(self.request.get_full_path())
			logging.info(url)
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
		logging.info(template_values)
		template_values.update(context)
		return template_values
