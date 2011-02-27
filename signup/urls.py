from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url (
        regex = '^email/$',
        view =  'signup.views.signup_email',
        name = 'signup_email'
        ),
   url (
        regex = '^logout/$',
        view =  'signup.views.signup_logout',
        name = 'signup_logout'
        ),
   url (
        regex = r'^$',
        view =  'signup.views.signup_login',
        name = 'signup_login'
        ),
    url (
        regex = '^login/$',
        view =  'signup.views.signup_login',
        name = 'signup_login'
        ),
      url (
        regex = '^login/email/(?P<user_id>[-\w]+)/(?P<token>[-\w]+)/$',
        view =  'signup.views.signup_login_by_email',
        name = 'signup_login_by_email'
        ),


    )