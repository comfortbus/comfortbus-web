# -*- coding: utf-8 -*-

from malha.models import Linha
from malha.models import Parada
from django.conf import settings
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import json
import urllib

@periodic_task(run_every=crontab(hour="2, 14", minute="0", day_of_week="1-5"))
def populate_linha():
    url = settings.API_BASE_URL + 'lines'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    for datum in data:
        try:
            linha = Linha.objects.get(id=datum['id'])
        except Linha.DoesNotExist:
            linha = Linha(id=datum['id'])

        if (linha.has_changes(datum)):
            linha.label = datum['label'].strip()
            linha.color = datum['color']
            linha.nome = datum['nombre'].strip()
        linha.save()

@periodic_task(run_every=crontab(hour="2, 14", minute="10", day_of_week="1-5"))
def populate_parada():
    for linha in Linha.objects.all():
        url = settings.API_BASE_URL + 'line/' + linha.label
        response = urllib.urlopen(url)
        try:
            data = json.loads(response.read())
        except ValueError:
            logger = populate_parada.get_logger()
            if response.read() != '':
                logger.error("URL '{}' return is incomprehensible".format(url))
                continue
            else:
                logger.warning("No data returned for URL '{}'".format(url))

        paradas = []
        for datum in data['stops']:
            try:
                parada = Parada.objects.get(id=datum['id'])
            except Parada.DoesNotExist:
                parada = Parada(id=datum['id'])

            if (parada.has_changes(datum)):
                parada.label = datum['label']
                parada.nome = datum['name']
                parada.lat = datum['location']['lat']
                parada.lon = datum['location']['lon']
                parada.save()

            if linha not in parada.linhas.all():
                parada.linhas.add(linha)

            paradas.append(parada)

        for parada in linha.paradas.all():
            if parada not in paradas:
                parada.linhas.remove(linha)