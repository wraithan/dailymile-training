from collections import defaultdict
from datetime import datetime, timedelta
import json
import math
from time import mktime

from django.db import models
import requests


def dailymile_api_get(action, params):
    url = 'https://api.dailymile.com/%s.json' % action
    return requests.get(url, params=params)


class DailyMileProfile(models.Model):
    user = models.OneToOneField('auth.User')
    access_token = models.CharField(max_length=255)

    def __unicode__(self):
        return self.user.username

    def get_entries(self):
        seven_days_ago = mktime((datetime.now()-timedelta(days=7)).timetuple())
        page = 1
        entries = []
        while True:
            res = dailymile_api_get('people/me/entries',
                                    params={
                                        'oauth_token': self.access_token,
                                        'since': seven_days_ago,
                                        'page': page,
                                    })
            retval = json.loads(res.content)
            if retval['entries']:
                entries.extend(retval['entries'])
                page += 1
            else:
                break
        return entries

    def stats_as_json(self):
        entries = self.get_entries()
        prepared_goals = {}
        for goal in self.goal_set.all():
            prepared_goals.update(goal.calculate_stats(entries))

        return json.dumps(prepared_goals)

class Goal(models.Model):
    owner = models.ForeignKey('core.DailyMileProfile')
    workout_type = models.CharField(max_length=255)
    goal = models.DecimalField(decimal_places=2, max_digits=7)

    def calculate_stats(self, entries):
        total = 0
        for entry in entries:
            if entry.has_key('workout'):
                activity_type = entry['workout']['activity_type']
                if self.workout_type == activity_type:
                    total += entry['workout']['distance']['value']
        return {self.workout_type: {'real': total, 'goal': str(self.goal)}}

    def __unicode__(self):
        return '%s: %s' % (self.workout_type, self.goal)