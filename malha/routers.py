# -*- coding: utf-8 -*-

from django.conf.urls import url
from malha.views import *

urlpatterns = [
    url(r'^linha/(?P<label>\w+)/$', linha_view, name='linha'),
    url(r'^linha/(?P<label>\w+)/veiculos/$', linhaveiculos_listview,
        name='linhaveiculos'),
    url(r'^parada/(?P<label>\w+)/$', parada_view, name='parada'),
    url(r'^parada/(?P<label>\w+)/estimativas/$', paradaestimativas_listview,
        name='paradaestimativas'),
    url(r'^paradas/$', parada_listview, name='paradas'),
    url(r'^veiculo/(?P<pk>\d+)/update/$', updatelotacao_view,
        name='update_lotacao'),
]
