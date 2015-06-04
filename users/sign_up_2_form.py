from django.db import models
from django.forms import ModelForm
from users.models import Users


class SignUp2Form(ModelForm):
    class Meta:
        model = Users
        fields = ['address','address2','city','state','zip','phone','first_name','last_name','email','password']

form = SignUp2Form()

class EditAddressForm(ModelForm):
    class Meta:
        model = Users
        fields = ['address','address2','city','state','zip','phone']

form = EditAddressForm()
