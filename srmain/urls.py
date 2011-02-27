from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url (
        regex = '^ride/map/(?P<ride_guid>[-\w]+)$',
        view =  'srmain.views.ride_map',
        name = 'ride_map'
        ),
    url (
        regex = '^rides/$',
        view =  'srmain.views.ride_list',
        name = 'ride_list'
        ),
    
       url(
        regex   = '^ride/list/$',
        view    = 'srmain.views.json_ride_list', 
        name    = 'json_ride_list' 
    ),
     
       url (
        regex = '^rider/$',
        view =  'srmain.views.rider_detail',
        name = 'rider_detail'
        ),
      url (
        regex = '^rider/(?P<rider_id>\d+)/$',
        view =  'srmain.views.rider_detail',
        name = 'rider_detail'
        ),
      
    # Add new data with POS 
    url(
        regex   = '^upload/$', 
        view    = 'srmain.views.upload_data', 
        name    = 'upload_data' 
    ),
    
    url(
        regex   = '^app/authenticate/$',
        view    = 'srmain.views.app_authenticate',
        name    = 'app_authenticate'
    ),
    
    url(
        regex = '^ping/show/$',
        view  = 'srmain.views.ping_show',
        name = 'ping_show'
    ),
    
    url(
        regex = '^ping/$',
        view  = 'srmain.views.ping',
        name = 'ping'
    ),
    
     url(
        regex = '^system/$',
        view  = 'srmain.views.system_map',
        name = 'system_map'
    ),
     
     url(
        regex   = '^route/save/$', 
        view    = 'srmain.views.save_route', 
        name    = 'save_route' 
    ),
     
      url(
        regex   = '^routes/$', 
        view    = 'srmain.views.route_list', 
        name    = 'route_list' 
    ),
      
       url(
        regex   = '^route/map/(?P<route_guid>[-\w]+)/$', 
        view    = 'srmain.views.route_map', 
        name    = 'route_map' 
    ),
     url(
        regex   = '^route/map/$', 
        view    = 'srmain.views.route_map', 
        name    = 'route_map' 
    ),
     
    url(
        regex   = '^route/json/(?P<route_guid>[-\w]+)/$',
        view    = 'srmain.views.json_route', 
        name    = 'json_route' 
    ),
      
    url(
        regex   = '^route/list/$',
        view    = 'srmain.views.json_route_list', 
        name    = 'json_route_list' 
    ),
     
    url (
        regex ='^ride/json/(?P<ride_guid>[-\w]+)/(?P<headers>[,\w]+)/$',
        view = 'srmain.views.json_ride',
        name = 'json_ride'
    ),
    
    url (
        regex ='^markers/fixed/$',
        view = 'srmain.views.fixed_markers',
        name = 'fixed_markers'
        ),
     
    url (
        regex ='^markers/all/$',
        view = 'srmain.views.all_markers',
        name = 'all_markers'
        ),
    )
    