import logging
from google.appengine.api import users, mail, taskqueue
from google.appengine.ext import webapp
from django import forms
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME



class MainView(TemplateView):
    template_name = 'guestbook/index.html'

    def get_context_data(self, *args, **kwargs):
        guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)
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

def send_mail(request):
    if request.method == 'POST':
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

class SignForm(forms.Form):
    guestbook_name = forms.CharField(
        label='Guestbook name',
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
    success_url="/sign/"
    def get_initial(self):
        initial = super(SignView, self).get_initial()
        guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        initial['guestbook_name']=guestbook_name
        return initial

    def form_valid(self, form):
        guestbook_name = form.cleaned_data['guestbook_name']
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = users.get_current_user()
        greeting.content = form.cleaned_data['guestkook_mesage']
        greeting.put()
        taskqueue.add(url = '/guestbook/sendmail',)
        messages.warning(self.request, '%s created successfully.' % guestbook_name)
        return super(SignView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Please input field!')
        return super(SignView, self).form_invalid(form)
