# -*- coding: utf-8 -*-

from django.conf.urls import url
from malha.views import *

urlpatterns = [
    url(r'^linha/(?P<label>\w+)/$', linha_view, name='linha'),
    url(r'^parada/(?P<label>\w+)/$', parada_view, name='parada'),
    url(r'^paradas/$', parada_listview, name='paradas')
]