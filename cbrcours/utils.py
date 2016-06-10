# -*- coding: utf-8 -*-
import requests
from time import sleep
from django.utils import timezone

requests_session = requests.session()


def read_url(url, RETRIES=3, RETRY_TIMEOUT=0.2, TIMEOUT=0.001, date=timezone.now):
    retry = 0
    while retry < RETRIES:
        if callable(date):
            date = date()
        try:
            response = requests.get(
                url % date.strftime("%d/%m/%Y"),
                timeout=TIMEOUT
            )
            return response
        except (
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError
        ):
            retry += 1
            if retry < RETRIES:
                sleep(RETRY_TIMEOUT)
    return
