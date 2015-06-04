from django.db import models

class SpecPizzaCandidateRecords(models.Model):

    user_id = models.IntegerField()
    pizza_order_id = models.IntegerField()
    interested_or_not = models.CharField(max_length=5,default="yes")    
