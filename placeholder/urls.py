# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls import patterns
from django.conf.urls import include

urlpatterns = patterns(
    'placeholder.views',
    url(r'^$', 'index'),
)