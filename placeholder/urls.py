# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls import patterns
from django.conf.urls import include
from placeholder.views import index

urlpatterns = [
    url(r'^$', index),
]