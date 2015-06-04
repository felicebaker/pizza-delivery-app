from django.db import models

class DriverPizzaOrders(models.Model):

    driver_id = models.IntegerField()
    pizza_order_id = models.IntegerField()

