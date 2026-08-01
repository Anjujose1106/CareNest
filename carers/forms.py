from django import forms
from .models import CarerApplication, CarerDocument


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

class CarerDocumentForm(forms.ModelForm):

    DOCUMENT_CHOICES = [
        ('DBS Certificate', 'DBS Certificate'),
        ('Right to Work', 'Right to Work'),
        ('Public Liability Insurance', 'Public Liability Insurance'),
        ('First Aid', 'First Aid'),
        ('Moving & Handling', 'Moving & Handling'),
        ('Safeguarding Adults', 'Safeguarding Adults'),
        ('Medication Administration', 'Medication Administration'),
        ('Dementia Awareness', 'Dementia Awareness'),
        ('Infection Control', 'Infection Control'),
        ('Autism Awareness', 'Autism Awareness'),
        ('Care Certificate', 'Care Certificate'),
        ('NVQ Level 2', 'NVQ Level 2'),
        ('NVQ Level 3', 'NVQ Level 3'),
    ]

    document_name = forms.ChoiceField(
        choices=DOCUMENT_CHOICES
    )

    class Meta:
        model = CarerDocument

        fields = [
            'document_name',
            'issue_date',
            'expiry_date',
            'file',
        ]

        labels = {
            'document_name': 'Certificate Name',
        }

        widgets = {
            'issue_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'expiry_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }