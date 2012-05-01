import json

from django.conf import settings
from django.contrib.auth.models import User
import requests

from training.core import DAILYMILE_TOKEN_URI, oauth2_token
from training.core.models import DailyMileProfile


class OAuth2Backend(object):
    """
    This backend takes an oauth2 authenticate code and sends it to
    the service in order to get the access_token.
    """

    support_object_permisions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, code=None):
        if code is None:
            return None
        else:
            auth_stuff = oauth2_token(DAILYMILE_TOKEN_URI,
                                      settings.DAILYMILE_CLIENT_ID,
                                      settings.DAILYMILE_CLIENT_SECRET,
                                      code,
                                      settings.DAILYMILE_REDIRECT_URI)

            api_endpoint='https://api.dailymile.com/'

            user_stuff = json.loads(requests.get(
                api_endpoint + 'people/me.json',
                params={'oauth_token': auth_stuff['access_token']}
            ).content)

            user = User.objects.filter(username=user_stuff['username'])

            if user.exists():
                user = user.get()
                profile = user.get_profile()
                profile.access_token = auth_stuff['access_token']
                profile.dailymile_url = user_stuff['url']
                profile.save()
            else:
                user = User.objects.create(
                    username=user_stuff['username'],
                    first_name=user_stuff['display_name'],
                    is_active=True, email=''
                )
                DailyMileProfile.objects.create(
                    user=user,
                    access_token=auth_stuff['access_token'],
                )

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
