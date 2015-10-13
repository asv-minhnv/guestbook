import logging
from django import forms
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from google.appengine.api import users

from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME


class MainView(TemplateView):
	template_name = 'guestbook/index.html'

	def get_context_data(self, *args, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(
			-Greeting.date)
		greetings = greetings_query.fetch(10)
		# logging.info(greetings)
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
		context = super(MainView, self).get_context_data(**kwargs)
		context['greetings'] = template_values
		return context


class SignForm(forms.Form):
	guestbook_name = forms.CharField(
        label='Gguestbook name',
        max_length=50
    )
	guestkook_mesage = forms.CharField(
        widget=forms.Textarea,
        label='Guestkook mesage',
        max_length=100
    )


class SignView(FormView):
    template_name = 'guestbook/sign.html'
    form_class = SignForm

    def get_initial(self):
        initial = super(SignView, self).get_initial()
        guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        # greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(
        # -Greeting.date)
        # greetings = greetings_query.fetch(10)
        # logging.info(greetings)
        if users.get_current_user():
            url = users.create_logout_url(self.request.get_full_path())
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.get_full_path())
            url_linktext = 'Login'

        template_data = {
            # 'greetings': greetings,
            'guestbook_name': guestbook_name,
        }
        initial['data_login']=template_data
        logging.info(initial)
        return initial

    def form_invalid(self, form):
        guestbook_name = self.request.POST.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.POST.get('content')
        greeting.put()
        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
