import logging
import urllib
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.api import taskqueue
from django.contrib import messages
from django import forms
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
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
			taskqueue.add(url = '/sign',params = {'email': user.email()},method = 'GET')
		return super(SignView, self).form_valid(form)

	def form_invalid(self, form):
		messages.warning(self.request, 'Please input field!')
		return super(SignView, self).form_invalid(form)


def send_mail(request):
	logging.info('begin')
	if request.method == 'GET':
		logging.info('begin 12')
		user = users.get_current_user()
		if user:
			message= mail.EmailMessage()
			message.sender=user.email()
			message.to = user.email()
			message.subject = 'Test'
			message.body= """
							Dear Albert:
							Your example.com account has been approved.  You can now visit
							http://www.example.com/ and sign in using your Google Account to
							access new features.
							Please let us know if you have any questions.
							The example.com Team
							"""
			message.send()
			logging.info(message)
			return HttpResponseRedirect('/')
	return HttpResponseRedirect('/')

# class SendmailView(TemplateView):
# 	logging.info('begin')
# 	# def get(self, request, *args, **kwargs):
# 		logging.info('begin 1')
# 		email = request.GET.get('email')
# 		if email:
# 			# message= mail.EmailMessage()
# 			# message.sender = email
# 			# message.to = email
# 			# message.subject = 'Test'
# 			# message.body= """
# 			# 				Dear Albert:
# 			# 				Your example.com account has been approved.  You can now visit
# 			# 				http://www.example.com/ and sign in using your Google Account to
# 			# 				access new features.
# 			# 				Please let us know if you have any questions.
# 			# 				The example.com Team
# 			# 				"""
# 			# message.send()
# 			logging.info(message)
# 			return HttpResponseRedirect('/sign')
# 		return HttpResponseRedirect('/')