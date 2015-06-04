from django.db import models

class PizzaTypes(models.Model):

    pizza_order_description = models.CharField(max_length=150)
    pizza_order_id = models.IntegerField()



