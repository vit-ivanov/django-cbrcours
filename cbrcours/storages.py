# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.conf import settings
from django.forms.models import model_to_dict

from .models import Currency, CurrencyLastUpdate

from django.utils import timezone


class BaseCBRStorage(object):
    """
        Base class for storages
    """
    def get_from_storage(self, currency_code):
        raise NotImplemented

    def set_to_storage(self, currencies_dict):
        raise NotImplemented

    def del_from_storage(self):
        raise NotImplemented


class CacheCBRStorage(BaseCBRStorage):
    cache_key = "CBR_course"
    cache_timeout = getattr(settings, "CBR_CACHE_TIMEOUT", 12*60*60)

    def get_from_storage(self, currency_code):
        """
            Get course from storage
        """
        idict = cache.get(self.cache_key)
        if idict:
            return idict.get(currency_code)
        return

    def set_to_storage(self, currencies_dict):
        """
            Save course info to storage
        """
        self.del_from_storage()
        cache.set(self.cache_key, currencies_dict, timeout=self.cache_timeout)

    def del_from_storage(self):
        """
            Remove course from storage
        """
        cache.delete(self.cache_key)


class MysqlCBRStorage(BaseCBRStorage):
    model = Currency

    def get_from_storage(self, currency_code):
        """
            Get course info from mysql database.
        """
        try:
            obj = Currency.objects.get(code=currency_code)
            return model_to_dict(obj)
        except Currency.DoesNotExist:
            return

    def set_to_storage(self, currencies_dict):
        """
            Data update or insert to database
        """
        for k, idict in currencies_dict.iteritems():
            try:
                obj = Currency.objects.get(code=k)
                for k, v in idict.iteritems():
                    setattr(obj, k, v)
                obj.save()
            except Currency.DoesNotExist:
                idict['code'] = k
                try:
                    Currency.objects.create(**idict)
                except:
                    pass
        lobj = CurrencyLastUpdate()
        lobj.last_update = str(timezone.now())
        lobj.save()

    def del_from_storage(self):
        """
            Remove course from database
        """
        Currency.objects.all().delete()


class MixinCBRStorage(BaseCBRStorage):
    mysqlStorage = MysqlCBRStorage()
    cacheStorage = CacheCBRStorage()
    deltaHours = 5

    def get_from_storage(self, currency_code):
        """
            Get course info from mysql database.
        """
        result = self.cacheStorage.get_from_storage(
            currency_code)
        if result:
            return {
                'storage': 'cache',
                'result': result
            }
        return {
            'storage': 'mysql',
            'result': self.mysqlStorage.get_from_storage(currency_code)
        }

    def set_to_storage(self, currencies_dict):
        """
            Data update or insert to database and cache
        """
        self.mysqlStorage.set_to_storage(currencies_dict)
        self.cacheStorage.set_to_storage(currencies_dict)

    def del_from_storage(self):
        """
            Remove course from database
        """
        self.del_from_storage()
        self.del_from_storage()
