from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import ModelForm


User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name","last_name","username","email")
        field_classes = {'username': UsernameField}