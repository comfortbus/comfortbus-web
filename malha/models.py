# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.crypto import get_random_string
from malha.utils import parse_timestamp

__all__ = ['Linha', 'Parada', 'Veiculo', 'ParadaVeiculo']


class Linha(models.Model):

    color = models.CharField(
        'Cor', blank=True, default='#000000', max_length=7)
    label = models.CharField(u'Código', max_length=5)
    nome = models.CharField('Nome', max_length=255)

    class Meta:
        verbose_name = "Linha"
        verbose_name_plural = "Linhas"

    def __unicode__(self):
        return u'{} ({})'.format(self.nome, self.label)

    def has_changes(self, datum):
        return any([
            self.color != datum['color'],
            self.label != datum['label'],
            self.nome != datum['nombre'],
        ])


class Parada(models.Model):

    label = models.CharField(u'Código', max_length=20)
    nome = models.CharField('Nome', max_length=255)
    linhas = models.ManyToManyField(Linha, related_name='paradas')
    lat = models.FloatField('Latitude', null=True, blank=True)
    lon = models.FloatField('Longitude', null=True, blank=True)

    class Meta:
        verbose_name = "Parada"
        verbose_name_plural = "Paradas"

    def __unicode__(self):
        return u'{}: {}'.format(self.label, self.nome)

    def has_changes(self, datum):
        return any([
            self.label != datum['label'],
            self.nome != datum['name'],
            self.lat != datum['location']['lat'],
            self.lon != datum['location']['lon'],
        ])


class Veiculo(models.Model):

    linha = models.ForeignKey(Linha, related_name='veiculos')
    lotacao = models.IntegerField(u'Lotação', default=0)
    secret_key = models.CharField('Secret Key', max_length=32, null=True,
                                  blank=True)
    lat = models.FloatField('Latitude', null=True, blank=True)
    lon = models.FloatField('Longitude', null=True, blank=True)
    paradas = models.ManyToManyField(
        Parada, through=u'ParadaVeiculo', related_name='veiculos')

    class Meta:
        verbose_name = u"Veículos"
        verbose_name_plural = u"Veículos"

    def __unicode__(self):
        return u'({}) {}'.format(self.pk, self.linha)

    def save(self):
        if self.secret_key is None:
            self.secret_key = get_random_string(length=32)
        super(Veiculo, self).save()

    def update_location(self, location):
        self.lat = location['lat']
        self.lon = location['lon']
        self.save()

    def update_estimations(self, datum, parada_label):
        try:
            parada_veiculo = ParadaVeiculo.objects.get(
                parada__label=parada_label, veiculo=self)
        except ParadaVeiculo.DoesNotExist:
            parada_veiculo = ParadaVeiculo(parada=Parada.objects.get(
                label=parada_label), veiculo=self)
        if datum['arrivalTime']:
            parada_veiculo.tempo_chegada = parse_timestamp(
                datum['arrivalTime'])
            parada_veiculo.tempo_saida = parse_timestamp(datum['exitTime'])
            parada_veiculo.instante = parse_timestamp(datum['instant'])
            parada_veiculo.distancia = datum['distance']
            parada_veiculo.nome_destino = datum['destinationName']
        else:
            parada_veiculo.tempo_chegada = None

        parada_veiculo.save()


class ParadaVeiculo(models.Model):
    parada = models.ForeignKey(Parada)
    veiculo = models.ForeignKey(Veiculo)
    tempo_chegada = models.DateTimeField(
        u'Hora de Chegada', null=True, blank=True)
    tempo_saida = models.DateTimeField(
        u'Hora de Saída', null=True, blank=True)
    instante = models.DateTimeField(
        u'Instante', null=True, blank=True)
    distancia = models.PositiveIntegerField(u'Distância', default=0)
    nome_destino = models.CharField(
        'Nome do Destino', null=True, blank=True, max_length=255)
