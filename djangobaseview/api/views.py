import json
import logging
import urllib
from django.views.generic.base import TemplateResponseMixin
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.api import taskqueue
from django.contrib import messages
from django import forms
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from guestbook.models import Greeting, Guestbook
from django.http import HttpResponse


# class JSONResponseMixin(object):
#
# 	response_class = HttpResponse
# 	def render_to_json_response(self, context, **response_kwargs):
# 		response_kwarg['content_type'] = 'application/json'
# 		return self.response_class(
# 			self.convert_context_to_json(context)
# 			**response_kwargs
# 		)
# 	def convert_context_to_json(selfs, context):
# 		return  json.dumps(context)
#
#


class IndexView(JSONResponseMixin, TemplateResponseMixin):
	# template_name = "guestbook/index.html"

	def render_to_json_response(self, context, **response_kwargs):
		# context = super(IndexView, self).get_context_data(**kwargs)
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
		data = serializers.serialize('json', template_values)
		return HttpResponse(data, mimetype="application/json")
		# return self.render_to_json_response(context, **response_kwargs)
	# template_name = "guestbook/index.html"
	#
	# def post(self, request, *args, **kwargs):
	# 	guestbook_name = request.POST.get('guestbook_name')
	# 	content = request.POST.get('content')
	# 	Greeting.add_greeting(content, guestbook_name)
	# 	return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
	#
	# def get_context_data(self, **kwargs):
	# 	context = super(IndexView, self).get_context_data(**kwargs)
	# 	guestbook_name = self.request.GET.get('guestbook_name',Guestbook.get_default_guestbook())
	# 	greetings = Greeting.get_latest(guestbook_name,10)
	# 	if users.get_current_user():
	# 		url = users.create_logout_url(self.request.get_full_path())
	# 		url_linktext = 'Logout'
	# 	else:
	# 		url = users.create_login_url(self.request.get_full_path())
	# 		url_linktext = 'Login'
	# 	template_values = {
	# 		'greetings': greetings,
	# 		'guestbook_name': guestbook_name,
	# 		'url': url,
	# 		'url_linktext': url_linktext,
	# 	}
	# 	template_values.update(context)
	# 	return template_values


class SignForm(forms.Form):
	guestbook_name = forms.CharField(
		label='Guestbook name',
		max_length=50
	)
	guestbook_mesage = forms.CharField(
		widget=forms.Textarea,
		label='Guestkook mesage',
		max_length=100
	)


class SignView(FormView):
	template_name = 'guestbook/sign.html'
	form_class = SignForm
	success_url = '/sign/'
	def get_initial(self):
		initial = super(SignView, self).get_initial()
		guestbook_name = self.request.GET.get('guestbook_name',Guestbook.get_default_guestbook())
		initial['guestbook_name'] = guestbook_name
		return  initial

	def form_valid(self, form):
		guestbook_name = form.cleaned_data['guestbook_name']
		content = form.cleaned_data['guestbook_mesage']
		Greeting.add_greeting(content, guestbook_name)
		messages.success(self.request, '%s created successfully.' % guestbook_name)
		user = users.get_current_user()
		if user:
			taskqueue.add(url = '/sendmail/',params = {'email': user.email()},method = 'GET')
		return super(SignView, self).form_valid(form)

	def form_invalid(self, form):
		messages.warning(self.request, 'Please input field!')
		return super(SignView, self).form_invalid(form)


class DeleteForm(forms.Form):
	guestbook_name = forms.CharField(
		widget=forms.HiddenInput(),
		label='Guestbook name',
		max_length=50
	)
	greeting_id = forms.IntegerField(
		widget=forms.HiddenInput(),
		label='Greeeting id ',
	)


class DeleteView(FormView):
	template_name = "guestbook/delete.html"
	form_class = DeleteForm
	success_url = '/'

	def get_initial(self):
		initial = super(DeleteView, self).get_initial()
		guestbook_name = self.request.GET.get('guestbook_name', Guestbook.get_default_guestbook())
		greeting_id = self.request.GET.get('id')
		# greeting = Greeting.get_greeting(guestbook_name, greeting_id)
		initial['guestbook_name'] = guestbook_name
		initial['greeting_id'] = greeting_id
		return initial

	def form_valid(self, form):
		guestbook_name = form.cleaned_data['guestbook_name']
		greeting_id = form.cleaned_data['greeting_id']
		Greeting.delete_greeting(guestbook_name, greeting_id)
		messages.success(self.request, 'Delete successfully greeting.')
		return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

	def form_invalid(self, form):
		messages.warning(self.request, 'Can not delete Greeting')
		return super(DeleteView, self).form_invalid(form)


class EditForm(forms.Form):
	guestbook_name = forms.CharField(
		widget=forms.HiddenInput(),
		label='Guestbook name',
		max_length=50
	)
	greeting_id = forms.IntegerField(
		widget=forms.HiddenInput(),
		label='Greeeting id ',
	)
	guestbook_mesage = forms.CharField(
		widget=forms.Textarea,
		label='Guestkook mesage',
		max_length=100
	)


class EditView(FormView):
	template_name = "guestbook/edit.html"
	form_class = EditForm
	success_url = '/'

	def get_initial(self):
		initial = super(EditView, self).get_initial()
		guestbook_name = self.request.GET.get('guestbook_name', Guestbook.get_default_guestbook())
		greeting_id = self.request.GET.get('id')
		greeting = Greeting.get_greeting(guestbook_name, greeting_id)
		initial['guestbook_name'] = guestbook_name
		initial['greeting_id'] = greeting_id
		initial['guestbook_mesage'] = greeting.content
		return initial

	def form_valid(self, form):
		guestbook_name = form.cleaned_data['guestbook_name']
		greeting_id = form.cleaned_data['greeting_id']
		content = form.cleaned_data['guestbook_mesage']
		Greeting.update_greeting(content, guestbook_name, greeting_id)
		messages.success(self.request, 'Edit successfully greeting.')
		return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

	def form_invalid(self, form):
		messages.warning(self.request, 'Can not edit Greeting')
		return super(EditView, self).form_invalid(form)


class SendmailView(TemplateView):
	def get(self, request, *args, **kwargs):
		email = request.GET.get('email')
		if email:
			message= mail.EmailMessage()
			message.sender = email
			message.to = email
			message.subject = 'Test'
			message.body= """
							Wellcom
							You creat Greeting
							"""
			message.send()
			# logging.info(message)
			return HttpResponseRedirect('/sign')
		return HttpResponseRedirect('/')