# -*- coding: utf-8 -*-

from malha.models import Linha
from malha.models import Parada
from malha.models import Veiculo
from malha.models import ParadaVeiculo
from django.conf import settings
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import task
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


@periodic_task(run_every=crontab(hour="2, 14", minute="10", day_of_week="1-5"))
def populate_veiculo():
    for linha in Linha.objects.all():
        url = settings.API_BASE_URL + 'line/' + linha.label + '/vehicles'
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

        for datum in data:
            try:
                veiculo = Veiculo.objects.get(id=datum['id'])
            except Veiculo.DoesNotExist:
                veiculo = Veiculo(id=datum['id'])
                veiculo.linha = linha
                veiculo.save()
                for parada in linha.paradas.all():
                    if parada not in veiculo.paradas.all():
                        parada_veiculo = ParadaVeiculo(
                            parada=parada, veiculo=veiculo)
                        parada_veiculo.save()


@task()
def update_linha_veiculo_location(linha_label):
    url = settings.API_BASE_URL + 'line/' + linha_label + '/vehicles'
    response = urllib.urlopen(url)
    try:
        data = json.loads(response.read())
    except ValueError:
        logger = populate_parada.get_logger()
        if response.read() != '':
            logger.error("URL '{}' return is incomprehensible".format(url))
            return
        else:
            logger.warning("No data returned for URL '{}'".format(url))

    for datum in data:
        try:
            veiculo = Veiculo.objects.get(id=datum['id'])
        except Veiculo.DoesNotExist:
            logger = populate_parada.get_logger()
            logger.error("Vehicle with ID '{}' not found".format(datum['id']))
            continue

        veiculo.update_location(datum['location'])


@task()
def update_parada_estimativas(parada_label):
    url = settings.API_BASE_URL + 'stop/' + parada_label + '/estimations'
    response = urllib.urlopen(url)
    try:
        data = json.loads(response.read())
    except ValueError:
        logger = populate_parada.get_logger()
        if response.read() != '':
            logger.error("URL '{}' return is incomprehensible".format(url))
            return
        else:
            logger.warning("No data returned for URL '{}'".format(url))

    for datum in data:
        try:
            veiculo = Veiculo.objects.get(id=datum['vehicle'])
        except Veiculo.DoesNotExist:
            logger = populate_parada.get_logger()
            logger.error(
                "Vehicle with ID '{}' not found".format(datum['vehicle']))
            continue

        veiculo.update_estimations(datum, parada_label)
