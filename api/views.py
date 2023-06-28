from rest_framework.views import Response
from rest_framework.decorators import api_view

from api.serializers import DrugSerializer
from dashboard.models import Drug


@api_view(['GET','POST'])
def drugApiView(request, pk=None):
    context = {}
    if not pk:
        if request.method == 'POST':
            serializer = DrugSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
            
            context['status'] = 200
            context['data'] = serializer.data
        
        if request.method == 'GET':
            drugs = Drug.objects.all()
            for drug in drugs:
                drug.quantity=drug.get_quantity()
                
            serializer = DrugSerializer(drugs, many=True)

            context['status'] = 200
            context['data'] = serializer.data

        
    return Response(context)
