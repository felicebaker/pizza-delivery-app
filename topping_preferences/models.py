from django.db import models

class ToppingPreferences(models.Model):
    topping_preference = models.CharField(max_length=50)
    #user_id = models.ForeignKey('users.Users')
    user_id = models.IntegerField()
