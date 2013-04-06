from datetime import datetime, timedelta
import json
from time import mktime

from django.db import models
from model_utils import Choices

from training.core.dailymile import api_get


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
            retval = api_get('people/me/entries',
                             params={
                                 'oauth_token': self.access_token,
                                 'since': seven_days_ago,
                                 'page': page,
                             }).json
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

    def friends(self):
        retval = api_get('/people/me/friends',
                         params={'oauth_token': self.access_token})
        usernames = [friend['username'] for friend in retval.json['friends']]
        return DailyMileProfile.objects.filter(user__username__in=usernames)


class Goal(models.Model):
    WORKOUT_TYPE = Choices(('cycling', 'Cycling'),
                           ('hiking', 'Hiking'),
                           ('running', 'Running'),
                           ('walking', 'Walking'),
                           ('swimming', 'Swimming'),)
    GOAL_TYPE = Choices(('total_distance', 'Total Distance'),
                        ('total_duration', 'Total Duration'),
                        ('workout_distance', 'Workout Distance'),
                        ('workout_duration', 'Workout Duration'),)
    total_goals = (GOAL_TYPE.total_distance, GOAL_TYPE.total_duration)
    count_goals = (GOAL_TYPE.workout_distance, GOAL_TYPE.workout_duration)
    duration_goals = (GOAL_TYPE.total_distance, GOAL_TYPE.workout_distance)
    distance_goals = (GOAL_TYPE.total_duration, GOAL_TYPE.workout_duration)
    owner = models.ForeignKey('core.DailyMileProfile')
    workout_type = models.CharField(choices=WORKOUT_TYPE, max_length=255)
    goal_type = models.CharField(choices=GOAL_TYPE, max_length=255)
    goal_amount = models.DecimalField(decimal_places=2, max_digits=7)
    goal_count = models.PositiveIntegerField(default=0)

    def calculate_stats(self, entries):
        valid_workouts = self.get_valid_workouts(entries)
        if self.goal_type == self.GOAL_TYPE.total_distance:
            real = self.calculate_total_distance_stats(valid_workouts)
        elif self.goal_type == self.GOAL_TYPE.workout_distance:
            real = self.calculate_workout_distance_stats(valid_workouts)
        elif self.goal_type == self.GOAL_TYPE.total_duration:
            real = self.calculate_total_duration_stats(valid_workouts)
        elif self.goal_type == self.GOAL_TYPE.workout_duration:
            real = self.calculate_workout_duration_stats(valid_workouts)

        if self.is_count_goal:
            goal = self.goal_count
        elif self.is_total_goal:
            goal = self.goal_amount
        return {'label': self.label,
                'real': real,
                'goal': str(goal)}

    def get_valid_workouts(self, entries):
        valid_workouts = []
        for entry in entries:
            if 'workout' in entry:
                workout = entry['workout']
                if self.get_workout_type_display() == workout['activity_type']:
                    valid_workouts.append(workout)
        return valid_workouts

    def calculate_total_distance_stats(self, valid_workouts):
        total = 0
        for workout in valid_workouts:
            if 'distance' in workout:
                total += workout['distance']['value']
        return round(total, 2)

    def calculate_workout_distance_stats(self, valid_workouts):
        total = 0
        for workout in valid_workouts:
            if 'distance' in workout:
                if workout['distance']['value'] >= self.goal_amount:
                    total += 1
        return total

    def calculate_total_duration_stats(self, valid_workouts):
        total = timedelta()
        for workout in valid_workouts:
            if 'duration' in workout:
                total += timedelta(seconds=workout['duration'])
        return round((total.seconds)/60, 2)

    def calculate_workout_duration_stats(self, valid_workouts):
        total = 0
        for workout in valid_workouts:
            if 'duration' in workout:
                if workout['duration'] >= self.goal_amount*60:
                    total += 1
        return total

    @property
    def is_duration_goal(self):
        return self.goal_type in self.duration_goals

    @property
    def is_distance_goal(self):
        return self.goal_type in self.distance_goals

    @property
    def is_total_goal(self):
        return self.goal_type in self.total_goals

    @property
    def is_count_goal(self):
        return self.goal_type in self.count_goals

    @property
    def units(self):
        if self.is_count_goal:
            return 'count'
        elif self.is_distance_goal:
            return 'in minutes'
        elif self.is_duration_goal:
            return 'in miles'

    @property
    def label(self):
        workout_type = self.get_workout_type_display()
        return "%(type)s (%(units)s)" % {'type': workout_type,
                                         'units': self.units}

    def __unicode__(self):
        return '%s: %s' % (self.workout_type, self.goal_amount)


class APICall(models.Model):
    when = models.DateTimeField(auto_now_add=True)
