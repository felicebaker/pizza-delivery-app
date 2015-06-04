from django.contrib import admin
from drivers.models import Drivers

class DriversAdmin(admin.ModelAdmin):
    list_display = ('driver_first_name','driver_last_name','driver_cell_phone','merchant_name')
admin.site.register(Drivers, DriversAdmin)

