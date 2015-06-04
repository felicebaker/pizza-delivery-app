from django.db import models

class PizzaOrders(models.Model):

    delivery_addr1 = models.CharField(max_length=300)
    delivery_addr2 = models.CharField(max_length=300,blank=True,null=True)
    delivery_city  = models.CharField(max_length=300)
    delivery_state = models.CharField(max_length=300)
    delivery_zip_code = models.CharField(max_length=30)
    merchant_name = models.CharField(max_length=30)
    spec_pizza_radius = models.CharField(max_length=30,blank=True,null=True)
    spec_pizza_type = models.CharField(max_length=30,blank=True,null=True)
    spec_pizza_price = models.DecimalField(decimal_places=2,max_digits=5,blank=True,null=True)
    order_placed_time_stamp_user_time_zone = models.BigIntegerField(blank=True,null=True)
    spec_pizza_vetting_begin = models.BigIntegerField(blank=True,null=True)
    spec_pizza_vetting_end = models.BigIntegerField(blank=True,null=True)
    spec_pizza_sold_yes_or_no = models.CharField(max_length=5,blank=True,null=True)
    
