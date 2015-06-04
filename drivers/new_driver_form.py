from django.db import models
from django.forms import ModelForm
from drivers.models import Drivers


class NewDriverForm(ModelForm):
    class Meta:
        model = Drivers
        fields = ['driver_first_name','driver_last_name','driver_cell_phone','merchant_name']

form = NewDriverForm()
