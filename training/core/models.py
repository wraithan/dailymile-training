from collections import defaultdict
from datetime import datetime, timedelta
import json
import math
from time import mktime

from django.db import models
import requests


class DailyMileProfile(models.Model):
    access_token = models.CharField(max_length=255)
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return self.user.username

    def update_stats(self):
        pass

    def stats_as_json(self):
        retval = {'Cycling': {'real': 0, 'goal': 100},
                  'Hiking': {'real': 0, 'goal': 5},
                  'Running': {'real': 0, 'goal': 3}
        }

        api_endpoint='https://api.dailymile.com/'
        seven_days_ago = mktime((datetime.now()-timedelta(days=7)).timetuple())
        entries = json.loads(requests.get(
            api_endpoint + 'people/me/entries.json',
            params={
                'oauth_token': self.access_token,
                'since': seven_days_ago}
        ).content)

        for entry in entries['entries']:
            if entry.has_key('workout'):
                activity_type = entry['workout']['activity_type']
                retval[activity_type]['real'] += entry['workout']['distance']['value']
        for key,val in retval.items():
            retval[key]['real'] = math.trunc(round(retval[key]['real']))
        return retval