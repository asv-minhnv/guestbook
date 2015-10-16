import logging
import urllib
from google.appengine.api import users
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from guestbook.models import Greeting


class IndexView(TemplateView):
	template_name = "guestbook/index.html"

	def post(self, request, *args, **kwargs):
		guestbook_name = request.POST.get('guestbook_name')
		content = request.POST.get('content')
		Greeting.add_greeting(content, guestbook_name)
		return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		guestbook_name = self.request.GET.get('guestbook_name', Greeting.get_default_guestbook())
		greetings = Greeting.get_latest(guestbook_name, 10)
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


class DetailView(TemplateView):
	template_name = "guestbook/detail.html"

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		guestbook_name = self.request.GET.get('guestbook_name', Greeting.get_default_guestbook())
		id = self.request.GET.get('id')
		greeting = Greeting.get_greeting(guestbook_name, id)
		template_values = {
			'greeting': greeting,
			'guestbook_name': guestbook_name,
		}
		template_values.update(context)
		return template_values

class DeleteView(TemplateView):
	template_name = "guestbook/delete.html"

	def post(self, request, *args, **kwargs):
		guestbook_name = request.POST.get('guestbook_name')
		id = request.POST.get('id')
		logging.info(guestbook_name)
		Greeting.delete(guestbook_name, id)
		return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

	def get_context_data(self, **kwargs):
		context = super(DeleteView, self).get_context_data(**kwargs)
		guestbook_name = self.request.GET.get('guestbook_name', Greeting.get_default_guestbook())
		id = self.request.GET.get('id')
		greeting = Greeting.get_greeting(guestbook_name, id)
		template_values = {
			'greeting': greeting,
			'guestbook_name': guestbook_name,
		}
		template_values.update(context)
		return template_values


class EditView(TemplateView):
	template_name = "guestbook/edit.html"

	def post(self, request, *args, **kwargs):
		guestbook_name = request.POST.get('guestbook_name')
		content = request.POST.get('content')
		id = request.POST.get('id')
		Greeting.update_greeting(content, guestbook_name, id)
		return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

	def get_context_data(self, **kwargs):
		context = super(EditView, self).get_context_data(**kwargs)
		guestbook_name = self.request.GET.get('guestbook_name', Greeting.get_default_guestbook())
		id = self.request.GET.get('id')
		greeting = Greeting.get_greeting(guestbook_name, id)
		template_values = {
			'greeting': greeting,
			'guestbook_name': guestbook_name,
		}
		template_values.update(context)
		return template_values