from django.shortcuts import render

from dashboard.models import ProductCategory

# Create your views here.
def homepageView(request):
    template_name = 'frontend/index.html'
    context = {}
    return render(request, template_name, context)

def contactpageView(request):
    template_name = 'frontend/contact.html'
    context = {}
    return render(request, template_name,context)

def servicepageView(request):
    template_name = 'frontend/services.html'
    context = {}
    return render(request, template_name,context)

def aboutpageView(request):
    template_name = 'frontend/about.html'
    context = {}
    return render(request, template_name,context)

def ordersView(request):
    template_name = 'frontend/orders.html'
    context = {}
    return render(request, template_name,context)

def productsView(request):
    template_name = 'frontend/products.html'
    categories = ProductCategory.objects.all()
    context = {
        "categories": categories
    }
    return render(request, template_name,context)

