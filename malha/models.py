# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

__all__ = ['Linha', 'Parada']

# Create your models here.
class Linha(models.Model):

    color = models.CharField(
        'Cor', blank=True, default='#000000', max_length=7)
    label = models.CharField(u'Código', max_length=5)
    nome = models.CharField('Nome', max_length=255)

    class Meta:
        verbose_name = "Linha"
        verbose_name_plural = "Linhas"

    def __unicode__(self):
        return u'{} - {}'.format(self.label, self.nome)

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