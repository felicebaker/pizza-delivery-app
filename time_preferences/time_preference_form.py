
from django.db import models
from django.forms import ModelForm
from time_preferences.models import TimePreferences


class TimePreferencesForm(ModelForm):
    class Meta:
        model = TimePreferences
        fields = ['time_preference','user_id']

form = TimePreferencesForm()

class TimePreferencesAdjustForm(ModelForm):
    class Meta:
        model = TimePreferences
        fields = ['time_preference','user_id']

form = TimePreferencesAdjustForm()
