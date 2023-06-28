from django import forms

from dashboard.models import Diagnosis, Patient



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = '__all__'

class DiagnosisFormFull(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = '__all__'

DiagnosisFormSet = forms.inlineformset_factory(Patient, Diagnosis, form=DiagnosisForm, extra=1, max_num=1)
