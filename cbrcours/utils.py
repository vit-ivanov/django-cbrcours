# -*- coding: utf-8 -*-
import requests
from time import sleep

requests_session = requests.session()


def read_url(url, RETRIES=3, RETRY_TIMEOUT=0.2, TIMEOUT=0.001):
    retry = 0
    while retry < RETRIES:
        try:
            response = requests.get(
                url,
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
