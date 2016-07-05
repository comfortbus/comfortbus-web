# -*- coding: utf-8 -*-

from malha.mixins import CSRFExemptMixin
from malha.models import *
from malha.serializers import *
from malha.tasks import update_linha_veiculo_location
from malha.tasks import update_parada_estimativas
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse
from django.views.generic import View
import json

__all__ = ['linha_view', 'parada_view', 'parada_listview',
           'linhaveiculos_listview', 'paradaestimativas_listview',
           'updatelotacao_view']


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


class UpdateLotacaoView(CSRFExemptMixin, View):
    def post(self, request, **kwargs):
        veiculo = Veiculo.objects.get(pk=kwargs['pk'])
        data = json.loads(request.body.decode("utf-8"))
        import ipdb; ipdb.set_trace()
        if veiculo.secret_key == data.get('secret_key', None):
            try:
                veiculo.lotacao = int(data['lotacao'])
            except KeyError:
                return HttpResponse(status=400)
            veiculo.save()
        else:
            return HttpResponse(status=403)
        return HttpResponse(status=204)


linha_view = LinhaAPIView.as_view()
parada_view = ParadaAPIView.as_view()
parada_listview = ParadaListAPIView.as_view()
linhaveiculos_listview = LinhaVeiculosAPIView.as_view()
paradaestimativas_listview = ParadaEstimativasAPIView.as_view()
updatelotacao_view = UpdateLotacaoView.as_view()
