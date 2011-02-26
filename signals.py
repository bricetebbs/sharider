from django.db.models.signals import post_save
from django.contrib.auth.models import User
from srmain.models import RiderProfile

def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = RiderProfile(user=user)
        profile.save()

post_save.connect(create_profile, sender=User, dispatch_uid="users-profilecreation-signal")
