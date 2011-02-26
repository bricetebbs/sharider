from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.db.models import  Max, Min
import csv
import os
import uuid

from django.conf import settings
    

class RiderProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    # Recent location
    recent_time = models.DateTimeField(null=True, blank=True)
    recent_latitude = models.FloatField(default = 0.0)
    recent_longitude = models.FloatField(default = 0.0)
    recent_heading = models.FloatField(default = 0.0) # 0 north 90 east 180 south 270 west
    recent_speed = models.FloatField(default = 0.0)
    
    def __unicode__(self):
        return self.user.username
    
    def dict_for_marker_json(self):
        return dict(latitude = self.recent_latitude,
                    longitude = self.recent_longitude,
                    kind = settings.MARKER_TYPE_RIDER,
                    name = self.user.username, 
                    link = reverse('rider_detail', args=[self.user.id]),
                    icon = settings.MARKER_INFO[settings.MARKER_TYPE_RIDER]['icon'],
                    hover = 'Time %s Speed %f' % (str(self.recent_time), self.recent_speed))
    
    
    
class Ride(models.Model):
    guid = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=200)
    rider = models.ForeignKey(User)
    start_time = models.DateTimeField(blank = True)
    end_time = models.DateTimeField(blank = True)
    distance = models.FloatField(default = 0.0)
    
    def min_latitude(self):
        agg = self.segment_set.aggregate(Min('min_latitude'))
        return agg['min_latitude__min']
    def max_latitude(self):
        agg = self.segment_set.aggregate(Max('max_latitude'))
        return agg['max_latitude__max']
    
    def min_longitude(self):
        agg = self.segment_set.aggregate(Min('min_longitude'))
        return agg['min_longitude__min']
    def max_longitude(self):
        agg = self.segment_set.aggregate(Max('max_longitude'))
        return agg['max_longitude__max']
        
    def min_altitude(self):
        agg = self.segment_set.aggregate(Min('min_altitude'))
        return agg['min_altitude__min']
    def max_altitude(self):
        agg = self.segment_set.aggregate(Max('max_altitude'))
        return agg['max_altitude__max']
    
    def max_speed(self):
        agg = self.segment_set.aggregate(Max('max_speed'))
        return agg['max_speed__max']
    
    def center_latitude(self):
        agg = self.segment_set.aggregate(Min('min_latitude'), Max('max_latitude'))
        if agg:
            return (agg['min_latitude__min'] + agg['max_latitude__max'])/2.0
        return 0.0
                            
    def center_longitude(self):
        agg = self.segment_set.aggregate(Min('min_longitude'), Max('max_longitude'))
        if agg:
            return (agg['min_longitude__min'] + agg['max_longitude__max'])/2.0
        return 0.0
    
    def html_distance(self):
        s = "%6.2f miles" % (self.distance*0.00062137119,)
        return s
    
    def html_duration(self):
        td = self.end_time-self.start_time
        return td
    
    def __unicode__(self):
        return self.guid + u':'  + unicode(self.start_time) + u":" + unicode(self.distance)
    
class Segment(models.Model):
    guid = models.CharField(max_length=40, primary_key=True)
    ride = models.ForeignKey(Ride)
    safety_level = models.IntegerField(default = 0, choices=((0, "No Data"),(10,"Safe"),(20,"Dicey in Spots"),(30, "Scary")))
    
    sample_count = models.IntegerField(default = 0)
    
    headers = models.CharField(max_length=100)
    
    distance = models.FloatField(default = 0.0)
    
    start_time = models.DateTimeField(blank = True)
    end_time = models.DateTimeField(blank = True)
    
    min_latitude = models.FloatField(blank = True)
    max_latitude = models.FloatField(blank = True)
    min_longitude= models.FloatField(blank = True)
    max_longitude = models.FloatField(blank = True)
    
    min_altitude = models.FloatField(blank=True)
    max_altitude = models.FloatField(blank=True)
    
    max_speed = models.FloatField(blank=True)
    
    def center_latitude(self):
        return (self.min_latitude+self.max_latitude)/2.0
    
    def center_longitude(self):
        return (self.min_longitude+self.max_longitude)/2.0
    
    def get_path(self):
        segment_folder = settings.SEGMENT_DIR + self.ride.rider.username + '/'
        if not os.path.exists(segment_folder):
            os.makedirs(segment_folder)
            
        return segment_folder + self.guid

    def samples_as_lat_long(self):
        seg_path = self.get_path()
        f = open(seg_path, "r")
        rval = []
        reader = csv.reader(f)
        for row in reader:
            rval.append((float(row[0]), float(row[1])))
        return rval
    
    def samples_as_distance_altitude_speed(self):
        harray = self.headers.split(',')
        didx = harray.index(u'DST')
        aidx = harray.index(u'ALT')
        sidx = harray.index(u'SPD')
        seg_path = self.get_path()
        f = open(seg_path, "r")
        rval = []
        reader = csv.reader(f)
        for row in reader:
            rval.append((float(row[didx]), float(row[aidx]), float(row[sidx])))
        return rval


    
    def __unicode__(self):
        return self.guid
    
class Marker(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField()
    hover_html = models.TextField(blank=True, null=True)
    kind = models.IntegerField(choices = settings.MARKER_TYPES)
    open_new_page = models.BooleanField(default = True)
    latitude = models.FloatField(default = 0.0)
    longitude = models.FloatField(default = 0.0)
    custom_icon = models.CharField(max_length = 100,blank=True, null=True)
    
    def __unicode__(self):
        return self.name + u':' + self.get_kind_display()
    
    def dict_for_json(self):
        return dict(latitude = self.latitude, longitude = self.longitude, kind = self.kind,
                    name = self.name, link = self.link,
                    icon = settings.MARKER_INFO[self.kind]['icon'],
                    hover = self.hover_html)
    

class Route(models.Model):
    guid = models.CharField(max_length=40, primary_key=True, blank = True)
    name = models.CharField(max_length = 200)
    kind = models.PositiveIntegerField(default = 0)
    creator = models.ForeignKey(User)
    created_time = models.DateTimeField(null=True, blank=True)
    modified_time = models.DateTimeField(null=True, blank=True)
    distance = models.FloatField(default = 0.0)
    
    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = uuid.uuid4()
        super(Route, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.name
    
    def min_latitude(self):
        agg = self.waypoint_set.aggregate(Min('latitude'))
        return agg['latitude__min']
    def max_latitude(self):
        agg = self.waypoint_set.aggregate(Max('latitude'))
        return agg['latitude__max']
    
    def min_longitude(self):
        agg = self.waypoint_set.aggregate(Min('longitude'))
        return agg['longitude__min']
    def max_longitude(self):
        agg = self.waypoint_set.aggregate(Max('longitude'))
        return agg['longitude__max']

        
class WayPoint(models.Model):
    route = models.ForeignKey(Route)
    order = models.PositiveIntegerField()
    latitude = models.FloatField(default = 0.0)
    longitude = models.FloatField(default = 0.0)
    

    
    
