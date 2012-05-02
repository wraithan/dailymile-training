from collections import defaultdict
from datetime import datetime, timedelta
import json
import math
from time import mktime

from django.db import models
from model_utils import Choices
import requests


def dailymile_api_get(action, params):
    url = 'https://api.dailymile.com/%s.json' % action
    return requests.get(url, params=params)


class DailyMileProfile(models.Model):
    user = models.OneToOneField('auth.User')
    dailymile_url = models.TextField()
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
            APICall.objects.create()
            retval = json.loads(res.content)
            if retval['entries']:
                entries.extend(retval['entries'])
                page += 1
            if len(retval['entries']) < 20:
                break
        return entries

    def stats_as_json(self):
        entries = self.get_entries()
        prepared_goals = []
        for goal in self.goal_set.all():
            prepared_goals.append(goal.calculate_stats(entries))

        return json.dumps(prepared_goals)

class Goal(models.Model):
    WORKOUT_TYPE = Choices(('cycling', 'Cycling'),
                           ('hiking', 'Hiking'),
                           ('running', 'Running'),
                           ('walking', 'Walking'),
                           ('swimming', 'Swimming'),)
    GOAL_TYPE = Choices(('total_distance', 'Total Distance'),
                        ('total_duration', 'Total Duration'),
                        ('workout_distance', 'Workout Distance'),
                        ('workout_duration','Workout Duration'),)
    owner = models.ForeignKey('core.DailyMileProfile')
    workout_type = models.CharField(choices=WORKOUT_TYPE, max_length=255)
    goal_type = models.CharField(choices=GOAL_TYPE, max_length=255)
    goal = models.DecimalField(decimal_places=2, max_digits=7)

    def calculate_stats(self, entries):
        if self.goal_type == self.GOAL_TYPE.total_distance:
            return self.calculate_total_distance_stats(entries)
        elif self.goal_type == self.GOAL_TYPE.total_duration:
            pass

    def calculate_total_distance_stats(self, entries):
        total = 0
        for entry in entries:
            if 'workout' in entry:
                workout = entry['workout']
                if self.get_workout_type_display() == workout['activity_type']:
                    if 'distance' in workout:
                        total += workout['distance']['value']
        return {'type': self.get_workout_type_display(),
                'real': round(total, 2),
                'goal': str(self.goal)}

    def __unicode__(self):
        return '%s: %s' % (self.workout_type, self.goal)

class APICall(models.Model):
    when = models.DateTimeField(auto_now_add=True)
