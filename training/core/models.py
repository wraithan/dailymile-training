from django.db import models


class DailyMileProfile(models.Model):
    oauth_user_id = models.CharField(max_length=20, blank=True, null=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return self.user.username
