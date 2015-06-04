from django.db import models

class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300,blank=True,null=True)
    city  = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    zip = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    entry_time_stamp = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=30)
    payment_profile_id_authnet = models.IntegerField(blank=True, null=True)
    profile_id_authnet =  models.IntegerField(blank=True, null=True)
    registration_confirmed = models.CharField(max_length=5, blank=True, null=True)
