# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import datetime, sys, inspect, importlib

from functools import wraps


from django.db import models
from rest_framework import serializers

from functools import wraps

from django.http import HttpResponseRedirect, HttpResponse

class Utils:
    @staticmethod
    def get_class(config, name: str) -> models.Model:
        return Utils.model_name_to_class(config[name])

    @staticmethod
    def get_manager(config, name: str) -> models.Manager:
        return Utils.get_class(config, name).objects

    @staticmethod
    def get_serializer(config, name: str):
        class Serializer(serializers.ModelSerializer):
            class Meta:
                model = Utils.get_class(config, name)
                fields = '__all__'

        return Serializer

    @staticmethod
    def model_name_to_class(name: str):

        model_name    = name.split('.')[-1]
        model_import  = name.replace('.'+model_name, '') 

        module = importlib.import_module(model_import)
        cls = getattr(module, model_name)

        return cls

    @staticmethod
    def get_model_name_from_path(path):
        return path.split('.')[-1]

def check_permission(function):
    @wraps(function)
    def wrap(viewRequest, *args, **kwargs):

        try:

            # Check user
            if viewRequest.request.user.is_authenticated:
                return function(viewRequest, *args, **kwargs)

            # All good - allow the processing
            return HttpResponseRedirect('/login/')

        except Exception as e:

            # On error
            return HttpResponse( 'Error: ' + str( e ) )

        return function(viewRequest, *args, **kwargs)

    return wrap
