import json
import logging
from django import forms
from django.http import HttpResponse, QueryDict
from django.views.generic.edit import FormView

from guestbook.models import Greeting, Guestbook


class JSONResponseMixin(object):
	def render_to_response(self, context):
		return self.get_json_response(self.convert_context_to_json(context))

	@staticmethod
	def get_json_response(content, **http_response_kwargs):
		return HttpResponse(content, content_type='application/json', **http_response_kwargs)

	@staticmethod
	def convert_context_to_json(context):
		return json.dumps(context)

class SignForm(forms.Form):
	guestbook_name = forms.CharField(
		label='Guestbook name',
		max_length=50,
		required = False
	)
	guestbook_mesage = forms.CharField(
		widget=forms.Textarea,
		label='Guestkook mesage',
		max_length=100
	)


class GetListView(JSONResponseMixin, FormView):

	form_class = SignForm
	def get(self, request, *args, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name',Guestbook.get_default_guestbook())
		count= 20
		url_safe = self.request.GET.get('cursor')
		logging.info(url_safe)
		greetings, next_cursor, is_more = Greeting.get_greeting_with_cursor(
			url_safe=url_safe,
			guestbook_name=guestbook_name,
		)
		data = {
			"guestbook_name": guestbook_name,
			"greetings": greetings,
			"more": is_more,
			"next_cursor": str(next_cursor.urlsafe()) if is_more else None
		}
		return self.render_to_response(data)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		# logging.info(form_class)
		if not form.is_valid():
			return HttpResponse(status=400)
		guestbook_name = self.request.GET.get('guestbook_name',Guestbook.get_default_guestbook())
		content = form.cleaned_data['guestbook_mesage']
		new_greeting = Greeting.add_greeting(content, guestbook_name)
		if new_greeting:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)


class EditForm(forms.Form):
	guestbook_mesage = forms.CharField(
		widget=forms.Textarea,
		label='Guestkook mesage',
		max_length=100,
	)


class ResourceSinge(JSONResponseMixin, FormView):

	form_class = EditForm
	def get(self, request, *args, **kwargs):
		guestbook_name = kwargs.get('guestbook_name',Guestbook.get_default_guestbook())
		greeting_id = kwargs.get('id', None)
		greeting = Greeting.get_greeting(guestbook_name, greeting_id)

		if not greeting:
			return HttpResponse(status=404)
		data = {
			"greeting_id": greeting.key.id(),
			"content": greeting.content,
			"date": str(greeting.date),
			"updated_by": str(greeting.author),
			"updated_date": str(greeting.update_date),
			"guestbook_name": guestbook_name,
		}
		return self.render_to_response(data)

	def put(self, request, *args, **kwargs):
		try:
			json_object = json.loads(self.request.body)

		except ValueError:
			self.request.POST = QueryDict(self.request.body)
		else:
			self.request.POST = json_object
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		update_greeting = self.update_resources(form, **kwargs)
		if update_greeting:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def delete(self, *args, **kwargs):
		guestbook_name = kwargs.get('guestbook_name',Guestbook.get_default_guestbook())
		greeting_id = kwargs.get('id', None)
		detete_greeting = Greeting.delete_greeting(guestbook_name, greeting_id)
		logging.info(guestbook_name)
		if detete_greeting is None:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)