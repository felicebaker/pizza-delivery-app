from django.db import models

class Drivers(models.Model):

    driver_first_name = models.CharField(max_length=30)
    driver_last_name = models.CharField(max_length=30)
    driver_cell_phone = models.CharField(max_length=30)
    merchant_name = models.CharField(max_length=30)
    
    class Meta:
            ordering = ['id']
            verbose_name_plural = "Drivers"

