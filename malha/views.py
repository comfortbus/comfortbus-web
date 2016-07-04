# -*- coding: utf-8 -*-

from malha.models import *
from malha.serializers import *
from malha.tasks import update_linha_veiculo_location
from malha.tasks import update_parada_estimativas
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView

__all__ = ['linha_view', 'parada_view', 'parada_listview',
           'linhaveiculos_listview', 'paradaestimativas_listview']


class LinhaAPIView(RetrieveAPIView):
    serializer_class = LinhaSerializer
    lookup_field = 'label'

    def get_queryset(self):
        return Linha.objects.filter(label=self.kwargs['label'])


class ParadaAPIView(RetrieveAPIView):
    serializer_class = ParadaSerializer
    lookup_field = 'label'

    def get_queryset(self):
        return Parada.objects.filter(label=self.kwargs['label'])


class ParadaListAPIView(ListAPIView):
    queryset = Parada.objects.all()
    serializer_class = ParadaListSerializer


class LinhaVeiculosAPIView(ListAPIView):
    serializer_class = LinhaVeiculosSerializer
    lookup_field = 'label'

    def get_queryset(self):
        update_linha_veiculo_location(self.kwargs['label'])
        return Veiculo.objects.filter(linha__label=self.kwargs['label'])


class ParadaEstimativasAPIView(ListAPIView):
    serializer_class = ParadaEstimativasSerializer
    lookup_field = 'label'

    def get_queryset(self):
        update_parada_estimativas(self.kwargs['label'])
        return ParadaVeiculo.objects.filter(
            parada__label=self.kwargs['label'], tempo_chegada__isnull=False)

linha_view = LinhaAPIView.as_view()
parada_view = ParadaAPIView.as_view()
parada_listview = ParadaListAPIView.as_view()
linhaveiculos_listview = LinhaVeiculosAPIView.as_view()
paradaestimativas_listview = ParadaEstimativasAPIView.as_view()
