# -*- coding: utf-8 -*-

from rest_framework import serializers
from malha.models import *

__all__ = ['LinhaSerializer', 'ParadaSerializer', 'ParadaListSerializer']

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
