from django.shortcuts import render
from rest_framework import viewsets
from malha.models import *
from malha.serializers import *
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView

__all__ = ['linha_view', 'parada_view', 'parada_listview']


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


linha_view = LinhaAPIView.as_view()
parada_view = ParadaAPIView.as_view()
parada_listview = ParadaListAPIView.as_view()
