# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import viewsets
from .models import Flow, FlowSerializer

class FlowViewSet( viewsets.ModelViewSet ):
    queryset=Flow.objects.all()
    serializer_class=FlowSerializer
    permission_classes=[]

    def perform_create( self, serializer ):
        return serializer.save( owner=self.request.user )
