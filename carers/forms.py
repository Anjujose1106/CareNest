from django import forms
from .models import CarerApplication


class CarerApplicationForm(forms.ModelForm):

    class Meta:
        model = CarerApplication

        fields = [
            'full_name',
            'email',
            'phone_number',
            'postcode',
            'experience_years',
            'care_type',
            'message',
        ]