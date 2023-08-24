from django import forms

# modelden çek
from .models import *

class CreateProfile(forms.ModelForm):

    class Meta:
        model = NetflixProfile
        fields = ["name", "avatar"]