# -*- coding: utf-8 -*-

from django.test import TestCase
from linha.tasks import populate
from linha.models import Linha

# Create your tests here.


class LinhaTest(TestCase):

    def setUp(self):
        self.nome_temp = u"Linha Ficticia que com certeza não existe"
        self.pk_temp = 1

    def test_population_instantiates(self):
        self.assertEqual(Linha.objects.all().count(), 0)
        populate()
        self.assertTrue(Linha.objects.all().count() > 300)
        self.pk_temp = Linha.objects.all().first().pk

    def test_population_updates(self):
        linha = Linha(id=self.pk_temp)
        linha.nome = self.nome_temp
        linha.label = "000"
        linha.color = "#101010"
        linha.save()
        populate()
        self.assertNotEqual(
            Linha.objects.get(pk=linha.pk).nome, self.nome_temp)
