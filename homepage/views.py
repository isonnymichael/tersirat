from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from homepage.models import Counter
from homepage.serializers import CounterSerializer
from rest_framework.decorators import api_view

from datetime import datetime  

from django.db.models import Sum

# Create your views here.
def addCounter(request):
    isExist = True
    count_data = JSONParser().parse(request)  

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    try:
        count = Counter.objects.get(creation_time=today)
    except Counter.DoesNotExist:
        isExist = False
        count_serializer = CounterSerializer(data=count_data)
        if count_serializer.is_valid():
            count_serializer.save() 
            return JsonResponse(count_serializer.data)

    if isExist:
        count_data['count'] = count.count + 1
        count_update_serializer = CounterSerializer(count, data=count_data)
        if count_update_serializer.is_valid():
            count_update_serializer.save()
            return JsonResponse(count_update_serializer.data)
         
    return JsonResponse(count_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):
    count_all = Counter.objects.all()
    count = Counter.objects.aggregate(Sum('count'))

    return render (request, 'index.html',{
        'count':count,
        'count_all':count_all
    })
