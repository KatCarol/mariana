from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import CreateView
from accounts.forms import SignupForm
from dashboard.mixins import AdminRequiredMixin

User = get_user_model()

# Auth and accounts
class SignupView(AdminRequiredMixin, CreateView):
    model = User
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def get_success_url(self):
        return reverse('dashboard:index')
