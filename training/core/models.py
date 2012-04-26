from django.db import models


class DailyMileProfile(models.Model):
    access_token = models.CharField(max_length=255)
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return self.user.username

    def update_stats(self):
        pass