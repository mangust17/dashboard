from .models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_models(request):
    models_qs = PricesClean.objects.all().values_list('model', flat=True).distinct().order_by('model')
    data = [{'label': model, 'value': model} for model in models_qs]
    return JsonResponse(data, safe=False)


