from django.db import models

class PizzaMerchants(models.Model):

    merchant_name = models.CharField(max_length=30)
    addr1 = models.CharField(max_length=300)
    addr2 = models.CharField(max_length=300,blank=True,null=True)
    city  = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    zip_code = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
            ordering = ['id']
            verbose_name_plural = "Pizza Merchants"

