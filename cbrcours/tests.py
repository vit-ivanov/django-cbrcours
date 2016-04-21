# -*- coding: utf-8 -*-
from django.test import TestCase
from mock import MagicMock

from .storages import CacheCBRStorage, MysqlCBRStorage
from .models import Currency
from .core import CBR_COURSE

from decimal import Decimal

import requests
import os
import codecs


main_dict = {
    u'USD': {
        'name': u'Доллар США',
        'value': Decimal(34.07),
        'nominal': 1,
    },
    u'EUR': {
        'name': u'Евро',
        'value': Decimal(46.41),
        'nominal': 1,
    },
    u'HUF': {
        'name': u'Венгерских форинтов',
        'value': Decimal(14.8596),
        'nominal': 100,
    },
}


def mock_get_request(url, timeout):
    response = requests.get.return_value
    response.encoding = 'utf8'
    response.url = u'%s' % url
    data_file = os.path.join(
        os.path.dirname(__file__), 'XML_daily.asp')
    response.text = codecs.open(data_file, 'r', 'cp1251').read()
    return response


class StoragesTest(TestCase):

    def test_cache_storage(self):
        storage = CacheCBRStorage()
        storage.set_to_storage(main_dict)
        V = storage.get_from_storage('EUR')
        self.assertEquals(46.41, V.get('value'))
        storage.del_from_storage()
        self.assertFalse(storage.get_from_storage('EUR'))

    def test_mysql_storage(self):
        storage = MysqlCBRStorage()
        storage.set_to_storage(main_dict)
        self.assertEquals(Currency.objects.all().count(), 3)
        self.assertEquals(
            storage.get_from_storage('USD').get('value'),
            Decimal(34.07).quantize(Decimal('.01'))
        )
        main_dict['USD'] = {
            'name': u'Доллар США',
            'value': Decimal(30.07),
            'nominal': 1
        }
        storage.set_to_storage(main_dict)
        self.assertEquals(
            storage.get_from_storage('USD').get('value'),
            Decimal(30.07).quantize(Decimal('.01'))
        )
        storage.del_from_storage()
        self.assertFalse(Currency.objects.all())

    def test_cbr_course(self):
        cbr = CBR_COURSE()
        requests.get = MagicMock(side_effect=mock_get_request)
        self.assertEquals(
            cbr.get('USD').get('value'),
            Decimal('33.8353').quantize(Decimal('.0001'))
        )
        self.assertEquals(Currency.objects.filter(code='USD')[0].value,
                          Decimal(33.8353).quantize(Decimal("0.0001")))

        self.assertEquals(
            cbr.calculate_price(100, 'USD'),
            Decimal(3383.53).quantize(Decimal('.0001'))
        )

