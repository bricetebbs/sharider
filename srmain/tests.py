"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from srmain.models import  Segment
import unittest
import hashlib
import random
from django.test.client import Client
from django.contrib.auth.models import User

from django.conf import settings

from srmain.views import DEFAULT_HEADERS

def get_guid():
    return hashlib.sha1(str(random.random())).hexdigest()

class MyFuncTestCase(unittest.TestCase):
    
    
    def setUp(self):
        settings.SEGMENT_DIR = settings.INSTALL_DIR + 'test_segments/'
    def testRideCreate(self):


        user = User.objects.create_user('bluetester', 'blue@northnitch.com', 'bluepass')
        
        c= Client()
        response = c.post('/sharider/app/authenticate/', {'username': 'bluetester', 'password': 'bluepass'})
        
        print "Response 1=",response
        
        ride_guid = get_guid()
        segment_guid = get_guid()
        samples = [
            47.80227781790985, -117.3900181807607, 1281021165.306141, 0, 555.8206176757812,  0 , 0,
            47.80206519419391, -117.3900102930843, 1281021168.306145, 23.61884498596191, 555.342956542968, -2.02237298377300, 7.872937572303422,
            47.80199766351269, -117.3900140116787, 1281021169.306211, 31.12314414978027, 555.219970703125, -1.63887168351164, 7.503803952019674,
            47.8019349002223,  -117.3900221880961, 1281021170.308309, 38.11953735351562, 555.021240234375, -2.84047009575297, 6.981745342108972
            ]
        # DEFAULT_HEADERS = ['LAT', 'LON', 'TIM', 'DST', 'ALT', 'GRD', 'SPD']
        headers = DEFAULT_HEADERS
        print "DEFH",headers
        
        response = c.post('/sharider/upload/', dict(ride_guid=ride_guid, 
                                                    segment_guid = segment_guid, 
                                                    headers = ",".join(headers),
                                                    samples = ",".join([str(x) for x in samples]))
                          )
        
        
        print "Response 2=",response
        
        
        segment = Segment.objects.get(pk = segment_guid)
     
        
        self.assertEquals(segment.ride.guid , ride_guid)


