from django.conf.urls.defaults import *
from django.contrib import admin

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^sharider/', include('sharider.srmain.urls')),
    (r'^signup/', include('sharider.signup.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'sharider.srmain.views.system_map'),
    
)
