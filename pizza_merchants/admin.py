from django.contrib import admin
from pizza_merchants.models import PizzaMerchants

class PizzaMerchantsAdmin(admin.ModelAdmin):
    list_display = ('merchant_name',)
admin.site.register(PizzaMerchants, PizzaMerchantsAdmin)
