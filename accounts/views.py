from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import CreateView
from accounts.forms import SignupForm

User = get_user_model()

# Auth and accounts
class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def get_success_url(self):
        return reverse('accounts:login')
