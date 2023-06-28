from django.shortcuts import render

# Create your views here.
def landingPageView(request):
   context = {}
   template_name = 'dashboard/landing.html'
   return render(request, template_name, context)

def stockDrugsView(request):
   context = {}
   template_name = 'dashboard/landing.html'
   return render(request, template_name, context)