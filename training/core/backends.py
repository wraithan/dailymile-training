from django.conf import settings
from django.contrib.auth.models import User

from core import DAILYMILE_TOKEN_URI, oauth2_token
from core.models import DailyMileProfile


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

            user = User.objects.filter(geoloqiprofile__oauth_user_id=auth_stuff['user_id'])
            if user.exists():
                user = user.get()
                profile = user.get_profile()
                profile.access_token=auth_stuff['access_token']
                profile.refresh_token=auth_stuff['refresh_token']
                profile.save()
            else:
                user = User.objects.create(username=auth_stuff['username'],
                                           first_name=auth_stuff['display_name'],
                                           is_active=True, email='')
                GeoloqiProfile.objects.create(user=user,
                                              oauth_user_id=auth_stuff['user_id'],
                                              access_token=auth_stuff['access_token'],
                                              refresh_token=auth_stuff['refresh_token'])

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
