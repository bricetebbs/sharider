# Create your views here.
import copy
import csv
import logging

from datetime import datetime

from django.conf import settings
from django.utils import simplejson
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.views.generic.list_detail import object_list


from srmain.models import Ride, Segment, Marker, RiderProfile, Route, WayPoint
from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import ListView

from django.contrib.auth.models import User

logger = logging.getLogger('sharider')

@login_required
def rider_detail(request, rider_id = None):
    if not rider_id:
        rider_id = request.user.id
    rider = get_object_or_404(User, pk=rider_id)
    
    return render(request, 'srmain/rider_detail.html', dict(rider=rider))



@login_required
def route_list(request):
    queryset = Route.objects.all()
    return object_list(request, queryset=queryset)
@login_required
def ride_list(request):
    queryset = Ride.objects.all()
    return object_list(request, queryset=queryset)
@login_required
def marker_list(request):
    queryset = Marker.objects.all()
    return object_list(request, queryset=queryset)


@login_required
def save_marker(request):

    json_data = simplejson.loads(request.raw_post_data)

    print json_data
    if json_data['pk']:
        marker = Marker.objects.get(pk=int(json_data['pk']))
    else:
        marker = Marker(creator=request.user)
    marker.link = json_data['link']
    marker.kind = int(json_data['kind'])
    marker.name = json_data['name']
    marker.latitude = float(json_data['latitude'])
    marker.hover_html = ''
    marker.custom_icon = ''
    marker.longitude = float(json_data['longitude'])


    marker.save()
    
    return HttpResponse(simplejson.dumps(dict(response='OK'), default=jsonhandler), mimetype='application/json');

@login_required
def ride_map(request, ride_guid):
    ride = get_object_or_404(Ride, guid=ride_guid)
    return render(request, 'srmain/system_map.html', dict(ride = ride,
                                                          marker_info = simplejson.dumps(settings.MARKER_INFO)))

@login_required
def system_map(request):
    return render(request, 'srmain/system_map.html', dict(marker_info = simplejson.dumps(settings.MARKER_INFO)))

@login_required
def marker_map(request, marker_id=None):
    marker_editing = False
    if marker_id:
        marker = get_object_or_404(Marker, pk=marker_id)
        if marker.creator == request.user:
            marker_editing = True
    else:
        marker = Marker(kind=settings.MARKER_TYPE_CAUTION)
        marker_editing = True
    return render(request, 'srmain/system_map.html', dict(marker = marker,
                                                          marker_info = simplejson.dumps(settings.MARKER_INFO),
                                                          marker_types = settings.EDITIABLE_MARKER_TYPES,
                                                          marker_editing=marker_editing))


@login_required
def route_map(request, route_guid = None):
    route_editing = False
    if route_guid:
        route = get_object_or_404(Route, pk=route_guid)
        if route.creator == request.user:
            route_editing = True
    else:
        route = Route(guid=None, pk=None)
        route_editing = True
    return render(request, 'srmain/system_map.html', dict(  marker_info = simplejson.dumps(settings.MARKER_INFO),
                                                            route = route,
                                                            route_editing=route_editing))

@login_required
def ping_show(request):
    return render(request, 'srmain/ping_show.html')


def jsonhandler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

def update_segment_data(segment, headers, samples, first_row):
    seg_path = segment.get_path()
    f = open(seg_path, "a")

    lati = headers.index(u'LAT')
    loni = headers.index(u'LON')
    alti = headers.index(u'ALT')
    spdi = headers.index(u'SPD')
    
    writer = csv.writer(f)
    for row in samples:
        latitude = row[lati]
        longitude = row[loni]
        speed = row[spdi]
        altitude = row[alti]

        # make a setter for min_max(segment,'latitude', latitude, force=first_row)
        if first_row or latitude < segment.min_latitude:
            segment.min_latitude = latitude
        if first_row or latitude > segment.max_latitude:
            segment.max_latitude = latitude

        if first_row or longitude < segment.min_longitude:
            segment.min_longitude = longitude
        if first_row or longitude > segment.max_longitude:
            segment.max_longitude = longitude

        if first_row or altitude < segment.min_altitude:
            segment.min_altitude = altitude
        if first_row or altitude > segment.max_altitude:
            segment.max_altitude = altitude

        if first_row or speed > segment.max_speed:
            segment.max_speed = speed
        first_row = False
        writer.writerow(row)

    f.close()


def new_data(request, ride_guid, ride_name, seg_guid, headers, samples):
    ride, ride_created = Ride.objects.get_or_create(guid = ride_guid, defaults=dict(rider=request.user))
    ride.name = ride_name

    segment, seg_created = Segment.objects.get_or_create(guid = seg_guid, defaults=dict(ride=ride))

    segment.headers = ",".join(headers)

    ti = headers.index(u'TIM')
    di = headers.index(u'DST')


    start_time = datetime.fromtimestamp(samples[0][ti])
    end_time = datetime.fromtimestamp(samples[-1][ti])


    distance = samples[-1][di] - samples[0][di]

    if ride_created or (ride.start_time > start_time):
        ride.start_time = start_time

    if ride_created or (ride.end_time < end_time):
        ride.end_time = end_time

    if seg_created or (segment.start_time > start_time):
        segment.start_time = start_time

    if seg_created or (segment.end_time < end_time):
        segment.end_time = end_time

    ride.distance =  samples[-1][di]
    segment.distance += distance
    first_row = segment.sample_count == 0
    segment.sample_count += len(samples)
    update_segment_data(segment, headers, samples,  first_row)

    ride.save()
    segment.save()



def app_authenticate(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse(simplejson.dumps(dict(response='OK'), default=jsonhandler), mimetype='application/json')
        else:
            return HttpResponse(simplejson.dumps(dict(response='DISABLED'), default=jsonhandler), mimetype='application/json')
    else:
        return HttpResponse(simplejson.dumps(dict(response='INVALID'), default=jsonhandler), mimetype='application/json')


DEFAULT_HEADERS = ['LAT', 'LON', 'TIM', 'DST', 'ALT', 'GRD', 'SPD']

@login_required
def upload_data(request):

    ride_guid = request.POST['ride_guid']
    seg_guid = request.POST['segment_guid']

    ride_name = request.POST.get('ride_name','')

    try:
        samples = request.POST[u'samples']
    except:
        samples = ""


    samples = samples.rstrip(',')
    if(samples):
        samples = [float(term) for term in samples.split(',')]

    try:
        headers = request.POST[u'headers']
        headers = headers.split(',')
    except:
        headers = DEFAULT_HEADERS

    hl = len(headers)
    if samples:
        samples = [samples[x*hl:x*hl+hl] for x in range(0, len(samples)/hl)]

    new_data(request, ride_guid, ride_name, seg_guid, headers, samples)
    return HttpResponse(simplejson.dumps(dict(response='OK'), default=jsonhandler), mimetype='application/json')




@login_required
def save_route(request):

    json_data = simplejson.loads(request.raw_post_data)

    name = json_data['name']
    way_points = json_data['points']
    distance = json_data['distance']
    guid = json_data['route_guid']

    ptime = datetime.now()
    if guid:
        route = Route.objects.get(pk = guid)
    else:
        route = Route(name = name, creator = request.user, created_time = ptime)

    route.modified_time = ptime
    route.name = name
    route.distance = distance
    route.save()

    WayPoint.objects.filter(route = route).delete()

    for o,p in enumerate(way_points):
        wp = WayPoint(route = route, order = o, latitude = p[0], longitude = p[1])
        wp.save()

    return HttpResponse(simplejson.dumps(dict(response='OK'), default=jsonhandler), mimetype='application/json')


def json_ride_list(request):
    ride_list = [ dict(name = ride.name, guid = ride.guid, rider=ride.rider.username) for ride in Ride.objects.all()]
    return HttpResponse(simplejson.dumps(dict(ride_list=ride_list)), mimetype='application/json')


def json_route(request, route_guid):
    route = get_object_or_404(Route, guid=route_guid)

    rval = dict(name = route.name,
                guid = route.guid,
                creator = route.creator.pk,
                wayPoints = [],
                bounds = dict(min_latitude = route.min_latitude(), min_longitude = route.min_longitude(),
                              max_latitude = route.max_latitude(), max_longitude = route.max_longitude())
                )

    for waypoint in route.waypoint_set.all().order_by('order'):
        rval['wayPoints'].append((waypoint.latitude, waypoint.longitude))

    return HttpResponse(simplejson.dumps(rval), mimetype='application/json')



def json_route_list(request):
    list_of_routes = [ dict(name = route.name, guid = route.guid, creator=route.creator.username) for route in Route.objects.all()]
    return HttpResponse(simplejson.dumps(dict(route_list=list_of_routes)), mimetype='application/json')


def fixed_markers(request):
    mlist = [x.dict_for_json() for x in Marker.objects.all()]

    marker_info = dict(markers=mlist, info_table = settings.MARKER_INFO)

    return HttpResponse(simplejson.dumps(marker_info),mimetype='application/json')

def all_markers(request):
    mlist = [x.dict_for_json() for x in Marker.objects.all()]
    mlist.extend( [x.dict_for_marker_json() for x in RiderProfile.objects.filter(recent_time__isnull=False)] ) # maybe also filter by time

    info = copy.deepcopy(settings.MARKER_INFO)
    info[settings.MARKER_TYPE_RIDER]['enabled'] = True
    marker_info = dict(markers=mlist, info_table = info)

    return HttpResponse(simplejson.dumps(marker_info),mimetype='application/json')


@login_required
def ping(request):
    profile = request.user.get_profile()
    profile.recent_time = datetime.now()
    profile.recent_latitude = float(request.POST['latitude'])
    profile.recent_longitude = float(request.POST['longitude'])
    profile.recent_header = float(request.POST['heading'])
    profile.recent_speed = float(request.POST['speed'])

    profile.save()
    return HttpResponse(simplejson.dumps(dict(response='OK'), default=jsonhandler), mimetype='application/json')


def json_ride(request, ride_guid, headers):
    ride = get_object_or_404(Ride, guid=ride_guid)
    headarr = headers.split(',')
    rval = dict(points=[], max_speed = ride.max_speed(),
                distance = ride.distance, min_altitude = ride.min_altitude(), max_altitude = ride.max_altitude(),
                 bounds = dict(min_latitude = ride.min_latitude(), min_longitude = ride.min_longitude(),
                              max_latitude = ride.max_latitude(), max_longitude = ride.max_longitude())
                )
    for segment in ride.segment_set.all():
        segheadarr = segment.headers.split(',')
        indicies = [segheadarr.index(x) for x in headarr]

        seg_path = segment.get_path()
        f = open(seg_path, "r")
        reader = csv.reader(f)
        for row in reader:
            rval['points'].append( [float(row[x]) for x in indicies])

    return HttpResponse(simplejson.dumps(rval), mimetype='application/json')


    
    
    
