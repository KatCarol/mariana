from django.urls import path

from frontend.views import aboutpageView, homepageView, contactpageView, servicepageView, ordersView, productsView

app_name = 'frontend'

urlpatterns = [
    path('', homepageView, name='homepage'),
    path('contact/', contactpageView, name='contact'),
    path('services/', servicepageView, name='services'),
    path('about/', aboutpageView, name='about'),
    path('orders/', ordersView, name='orders'),
    path('products/', productsView, name='products'),
]