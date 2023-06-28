from django import forms

from dashboard.models import Diagnosis, Patient



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        exclude = ('patient',)

class DiagnosisFormFull(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = '__all__'
