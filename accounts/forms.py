from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import ModelForm


User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name","last_name","username","email","is_clinician","is_sales_attendant","is_admin")
        field_classes = {'username': UsernameField}
        help_texts = {
            'is_clinician': ('Select to give the user access to clinic pages.'),
            'is_sales_attendant': ('Select to give the user access to sales pages.'),
            'is_admin': ('Select to give the user access to all pages.'),
        }