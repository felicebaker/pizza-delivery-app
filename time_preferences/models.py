from django.db import models

class TimePreferences(models.Model):

    time_preference = models.CharField(max_length=50)
    user_id = models.IntegerField()
