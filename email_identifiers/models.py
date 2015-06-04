from django.db import models

class EmailIdentifiers(models.Model):
    email_address = models.CharField(max_length=100)
    email_identifier = models.CharField(max_length=50)
