# -*- coding: utf-8 -*-
from django.conf import settings

from xmltodict import parse
from .utils import read_url

from .storages import MixinCBRStorage

from decimal import Decimal, ROUND_UP

from django.utils import timezone
from .models import CurrencyLastUpdate


class CBR_COURSE(object):
    """
        Class to store all information from http://www.cbr.ru/
        Convert currency
    """
    RETRIES = getattr(settings, "CBR_RETRIES", 3)
    RETRY_TIMEOUT = getattr(settings, "CBR_RETRY_TIMEOUT", 0.2)
    TIMEOUT = getattr(settings, "CBR_TIMEOUT", 5)

    CBR_URL = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s'

    STORAGE = MixinCBRStorage()

    def get_cbr_currency(self, date=timezone.now):
        '''
        Returns:
            None if no responce from server
            python dict
        '''
        response = read_url(
            self.CBR_URL,
            self.RETRIES,
            self.RETRY_TIMEOUT,
            self.TIMEOUT,
            date
        )
        if response:
            cbr = parse(response.text)
            valutes_dict = {}
            for valute in cbr['ValCurs']['Valute']:
                valutes_dict[valute['CharCode']] = {
                    'name': valute['Name'],
                    'value': Decimal(valute['Value'].replace(',', '.')).quantize(Decimal("0.0001")),
                    'nominal': int(valute['Nominal'])
                }
            return valutes_dict
        return

    def check_valid_answer(self, date=timezone.now):
        """
            Check if need update
        """
        if callable(date):
            date = date()
        try:
            obj = CurrencyLastUpdate.object.get(pk=1)
            delta = date - obj.last_update
            if delta < self.deltaHours:
                return False
        except CurrencyLastUpdate.DoesNotExist:
            pass
        return True

    def get(self, code):
        data = self.STORAGE.get_from_storage(code)
        if data.get('storage') != 'cache' or not data.get('result'):
            self.update_data()
            data = self.STORAGE.get_from_storage(code)
        return data.get('result')

    def update_data(self, date=timezone.now):
        """
            Update DATA
        """
        idict = self.get_cbr_currency(date=date)
        if idict:
            self.STORAGE.set_to_storage(idict)

    def calculate_price(self, price, currency):
        price = Decimal(price)
        currency = self.get(currency)
        price = price * currency.get('value') / (currency.get('nominal') or 1)
        return price.quantize(Decimal("0.01"), rounding=ROUND_UP)
