# -*- coding: utf-8 -*-
"""
Get curse from cbr.ru
"""
from .core import CBR_COURSE

_all__ = [
    'get_course', 'conver_price'
]


def get_course(CharCode):
    backend_cls = CBR_COURSE()
    return backend_cls.get(CharCode)


def conver_price(price, CharCode):
    backend_cls = CBR_COURSE()
    return backend_cls.calculate_price(price, CharCode)
