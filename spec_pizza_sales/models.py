from django.db import models

class SpecPizzaSales(models.Model):

    spec_pizza_type_name = models.CharField(max_length=30)
    spec_pizza_price = models.DecimalField(decimal_places=2,max_digits=5,blank=True,null=True)
    pizza_type_id = models.IntegerField()
    user_id = models.IntegerField()
    addr1 = models.CharField(max_length=300)
    addr2 = models.CharField(max_length=300,blank=True,null=True)
    city  = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    zip_code = models.CharField(max_length=30)
    delivery_time_stamp_user_time_zone = models.BigIntegerField(blank=True, null=True)
    

