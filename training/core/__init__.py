import json
from urllib import urlencode

import requests


DAILYMILE_AUTH_URI = 'https://api.dailymile.com/oauth/authorize'
DAILYMILE_TOKEN_URI = 'https://api.dailymile.com/oauth/token'


def oauth2_url(auth_uri, client_id, redirect_uri):
    return auth_uri + '?' + urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
    })


def oauth2_token(token_uri, client_id, client_secret, code, redirect_uri):
    payload = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    res = requests.post(token_uri, data=payload)
    return json.loads(res.content)
