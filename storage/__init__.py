import os

import requests

def store_file(origin, dest):
    if not _internet_on():
        os.rename(origin, dest)


def _internet_on():
    try:
        response = requests.head('https://google.com')
        response.raise_for_status()
        return True
    except Exception as err:
        print(err)
        return False
