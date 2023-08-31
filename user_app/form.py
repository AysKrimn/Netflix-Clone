from django import forms

from .models import NetflixProfile

class CreateProfile(forms.ModelForm):

      class Meta:
        
        model = NetflixProfile
        fields = ["name", "avatar"]

      def __init__(self, *args, **kwargs):
        super(CreateProfile, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            

