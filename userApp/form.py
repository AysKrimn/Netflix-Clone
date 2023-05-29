from django import forms
from .models import NetflixProfile

# form oluştur
class CreateProfile(forms.ModelForm):
         class Meta:
                model=NetflixProfile
                fields=['name', 'avatar']


