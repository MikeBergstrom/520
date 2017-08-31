# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login.models import User
class TripManager(models.Manager):
    def add(self, data, id):
        # results = {'status':True, 'errors':[]}
        # if not data['start']:
        #     results['errors'].append("Please enter a starting point")
        #     results['status'] = False
        # if not data['end']:
        #     results['errors'].append("Please enter a starting point")
        #     results['status'] = False
        # if results['status']:
        Trip.objects.create(
                name=data['name'],
                origin=data['start'],
                destination=data['end'],
                creator=User.objects.get(id=id)
            )
        return
# Create your models here.
class Trip(models.Model):
    name = models.CharField(max_length=500)
    origin = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    creator =models.ForeignKey('login.user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()