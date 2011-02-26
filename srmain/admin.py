from srmain.models import  Segment, Ride, RiderProfile,Marker, Route, WayPoint
from django.contrib import admin


class SegmentInline(admin.StackedInline):
    model = Segment


class RideAdmin(admin.ModelAdmin):
    inlines = [
        SegmentInline,
    ]
    list_display = ('name', 'rider', 'start_time')
    date_hierarchy = 'start_time'

    
class WayPointInline(admin.StackedInline):
    model = WayPoint

class RouteAdmin(admin.ModelAdmin):
    inlines = [
        WayPointInline,
    ]
    date_hierarchy = 'created_time'
    list_display = ('name', 'creator', 'created_time')

class WayPointAdmin(admin.ModelAdmin):
    list_display = ('route', 'latitude', 'longitude')
    
admin.site.register(Ride, RideAdmin)
admin.site.register(Segment)
admin.site.register(RiderProfile)
admin.site.register(Marker)
admin.site.register(Route, RouteAdmin)
admin.site.register(WayPoint, WayPointAdmin)