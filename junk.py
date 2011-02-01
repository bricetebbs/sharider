from django.test.client import Client
c = Client()
c.post('/sharider/ride/add/', dict(guid='dsds'))