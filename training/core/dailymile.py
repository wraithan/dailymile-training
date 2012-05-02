import requests
import json

from django.db.models import get_model


def api_get(call, params=None):
    api_endpoint = 'https://api.dailymile.com/'
    res = requests.get(
        api_endpoint + call + '.json',
        params=params
    )
    res.json = json.loads(res.content)
    get_model('core', 'APICall').objects.create()
    return res
