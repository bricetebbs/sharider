from django.template import RequestContext, loader
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404


def render_my_response(request, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)
    print "FOO",request
    return HttpResponse(loader.render_to_string(*args, **kwargs))
