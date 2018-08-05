# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
import datetime

class CreatedModel( models.Model ):
    created=models.DateTimeField( editable=False, default=datetime.datetime.now )

    class Meta:
        abstract=True

class Flow( CreatedModel ):
    owner=models.ForeignKey( User, related_name="flows" )
    text=models.CharField( max_length=255, blank=True, default="" )
    complete=models.BooleanField( default=False, blank=True )
    index=models.IntegerField( default=0, blank=True )
    parent=models.ForeignKey( 'self', related_name="children", null=True, blank=True )
    icon=models.CharField( max_length=50, default="bulllet", blank=True )

class FlowSerializer( serializers.ModelSerializer ):
    class Meta:
        model=Flow
        fields=('id', 'created', 'text','complete','index','parent', 'icon',)

class FlowShare( CreatedModel ):
    flow=models.ForeignKey( Flow, related_name="shares" )
    user=models.ForeignKey( User, related_name="shares" )
    editor=models.BooleanField( default=True, blank=True )

class FlowShareSerializer( serializers.ModelSerializer ):
    class Meta:
        model=FlowShare
        fields=('id','created','flow', 'editor',)
