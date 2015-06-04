from django.db import models
from django.forms import ModelForm
from email_identifiers.models import EmailIdentifiers


class EmailIdentifierForm(ModelForm):
    class Meta:
        model = EmailIdentifiers
        fields = ['email_identifier']

form = EmailIdentifierForm()

