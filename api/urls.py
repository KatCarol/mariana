from django.urls import path

from api.views import drugApiView

app_name = 'api'

urlpatterns = [
    path('drugs/', drugApiView, name='drugs'),
]