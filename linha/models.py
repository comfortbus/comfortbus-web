# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

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

    