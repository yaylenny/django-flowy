from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

import json
from flows.models import Flow, FlowSerializer

def initialData( user ):
    ''' this is used to get the full application data on page load '''
    if not user.flows.count():
        user.flows.create( text=" ")
    flows=user.flows.all()
    return {
        "user": { "name": user.username, "id": user.pk },
        "flows": FlowSerializer( flows, many=True ).data,
    }

class IndexView( TemplateView ):
    @method_decorator( login_required )
    def dispatch( self, request, *args, **kwargs ):
        if request.is_ajax():
            ''' a request for initial data from a javscript application'''
            data=initialData( request.user )
            return JsonResponse( data )
        return TemplateView.dispatch( self, request, *args, **kwargs )

    def get_template_names( self, **kwargs ):
        name="flowy.html" if self.request.user.is_authenticated() else "index.html"
        return [ name, ]

class UserHomeView( DetailView ):
    slug_field="username"
    slug_url_kwarg="username"
    template_name="user.html"
    model=User


    def get_context_data( self, *args, **kwargs ):
        ctx=super( UserHomeView, self ).get_context_data( *args, **kwargs )
        ctx.update({
        })
        return ctx
