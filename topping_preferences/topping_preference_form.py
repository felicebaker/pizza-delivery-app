
from django.db import models
from django.forms import ModelForm
from topping_preferences.models import ToppingPreferences

class ToppingPreferencesForm(ModelForm):
    class Meta:
        model = ToppingPreferences
        fields = ['topping_preference','user_id']

form = ToppingPreferencesForm()

class ToppingPreferencesAdjustForm(ModelForm):
    class Meta:
        model = ToppingPreferences
        fields = ['topping_preference','user_id']

form = ToppingPreferencesAdjustForm()

