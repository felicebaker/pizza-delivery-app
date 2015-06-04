from django.db import models

class Addresses(models.Model):

    addr1 = models.CharField(max_length=300)
    addr2 = models.CharField(max_length=300,blank=True,null=True)
    city  = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    zip_code = models.CharField(max_length=30)
    user_id = models.IntegerField(blank=True,null=True)   
    specpizzasales_id = models.IntegerField(blank=True,null=True)
    primarydeliveries_id = models.IntegerField(blank=True,null=True)
    merchants_id = models.IntegerField(blank=True,null=True)
    
    class Meta:
            ordering = ['id']
            verbose_name_plural = "Addresses"
