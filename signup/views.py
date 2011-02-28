# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import loader, Context

from django.contrib.sites.models import get_current_site

from django.utils.http import int_to_base36

from django.contrib.auth import login as login_user

from django.contrib.auth.views import login as login_view
from django.contrib.auth.views import logout as logout_view

from django.conf import settings

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import ugettext as _



class SignupEmailForm(forms.Form):
    email_address = forms.EmailField()


def send_email_auth_token(request, user, new_user=False):
    token_generator = PasswordResetTokenGenerator()
    site_name = get_current_site(request)
    t = loader.get_template('signup/email_auth_form.html')
    c = {
            'email': user.email,
            'site_name': site_name,
            'uid': int_to_base36(user.id),
            'user': user,
            'token': token_generator.make_token(user),
            'new_user' : new_user,
        }
    send_mail(_("New Login token for %s") % site_name, t.render(Context(c)), 'blue@northnitch.com',
                  [user.email])

def signup_email(request):
    email_form = SignupEmailForm(request.POST)
    if email_form.is_valid():
        email = email_form.cleaned_data['email_address']
        email = email.strip().lower()
        user = User.objects.filter(email=email)
        if user:
            # we had this guy before reset his password
            send_email_auth_token(request, user[0], new_user=False)
        else:
            user =  User.objects.create_user(email, email, '')
            send_email_auth_token(request, user, new_user=True)

    return HttpResponse('Check your email %s for a login token.' % email)

#
#  We can override the templates in here
#
def signup_login(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    email_form = SignupEmailForm
    return login_view(request, template_name='signup/login_main.html',
                    extra_context=dict(email_form=email_form))

def signup_logout(request):
    return logout_view(request, template_name='signup/logged_out.html')

def signup_login_by_email(request, user_id, token):
    user = get_object_or_404(User,pk=user_id)
    token_generator = PasswordResetTokenGenerator()

    if token_generator.check_token( user, token):
        user.backend='django.contrib.auth.backends.ModelBackend'
        login_user(request, user)

        return redirect(settings.LOGIN_REDIRECT_URL)
    return HttpResponse('Bad Link')