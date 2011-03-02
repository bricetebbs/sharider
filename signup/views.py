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
from django.contrib.auth.views import password_change as password_change_view

from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import ugettext as _

from django.contrib.auth.decorators import login_required



class SignupEmailForm(forms.Form):
    email_address = forms.EmailField(widget=forms.TextInput(attrs={'size':'45'}))


def send_email_auth_token(request, user, new_user=False):
    token_generator = PasswordResetTokenGenerator()
  
    t = loader.get_template('signup/email_auth_form.html')
    c = {
            'email': user.email,
            'host':  request.get_host(),
            'uid': int_to_base36(user.id),
            'user': user,
            'token': token_generator.make_token(user),
            'new_user' : new_user,
        }
    send_mail(_("New Login token for %s") % request.get_host(), t.render(Context(c)), settings.EMAIL_HOST_USER, [user.email])

def signup_email(request):
    email_form = SignupEmailForm(request.POST)
    if email_form.is_valid():
        email = email_form.cleaned_data['email_address']
        email = email.strip().lower()
        user = User.objects.filter(email=email)
        new_user = True
        if user:
            # we had this guy before reset his password
            send_email_auth_token(request, user[0], new_user=False)
            new_user = False
        else:
            user =  User.objects.create_user(email, email, '')
            send_email_auth_token(request, user, new_user=True)

        return render(request, 'signup/email_sent.html', dict(email=email, new_user=new_user))
    else:
         return login_view(request, template_name='signup/login_main.html',
                    extra_context=dict(email_form=email_form))


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
    return HttpResponse('Your login link has expired or is invalid. Please select a new one.')

class UserUpdateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['autocomplete']='off'

    def clean_username(self):
        if self.cleaned_data["username"] == self.instance.email:

            raise forms.ValidationError(_("Choose something other than your email address for the username"))

        if self.instance.username != self.instance.email: # then we have set if before
            raise forms.ValidationError(_("We have already set the username for this user before."))

        return super(UserUpdateForm, self).clean_username()

@login_required
def signup_change_username_and_password(request):
    if request.method=='GET':
        user_form = UserUpdateForm(instance=request.user)
    else:
        user_form = UserUpdateForm(request.POST,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)


    return render(request, 'signup/change_username_and_password.html', dict(user_form=user_form))

@login_required
def signup_change_password(request):
    return password_change_view(request, template_name='signup/change_password.html',
                                post_change_redirect=settings.LOGIN_REDIRECT_URL)

