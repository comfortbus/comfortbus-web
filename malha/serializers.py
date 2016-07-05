# -*- coding: utf-8 -*-

from rest_framework import serializers
from malha.models import *

__all__ = ['LinhaSerializer', 'ParadaSerializer', 'ParadaListSerializer',
           'LinhaVeiculosSerializer', 'ParadaEstimativasSerializer']


class LinhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linha


class ParadaSerializer(serializers.ModelSerializer):
    linhas = LinhaSerializer(read_only=True, many=True)

    class Meta:
        model = Parada


class ParadaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parada
        exclude = ('linhas', )


class LinhaVeiculosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        exclude = ('secret_key', 'linha',)


class ParadaEstimativasSerializer(serializers.ModelSerializer):
    lotacao = serializers.IntegerField(
        source='veiculo.lotacao', read_only=True)

    class Meta:
        model = ParadaVeiculo
        fields = (
            'veiculo', 'lotacao', 'tempo_chegada', 'tempo_saida',
            'instante', 'distancia', 'nome_destino')
