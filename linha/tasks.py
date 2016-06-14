# -*- coding: utf-8 -*-

from linha.models import Linha
from django.conf import settings
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import json
import urllib

@periodic_task(run_every=crontab(hour="2, 14", minute="0", day_of_week="1-5"))
def populate():
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