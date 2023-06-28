from django.urls import include, path

from dashboard.views import landingPageView

app_name = 'dashboard'

urlpatterns = [
   path('', landingPageView, name='landing'),
]