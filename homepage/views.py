from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from homepage.models import Counter
from homepage.serializers import CounterSerializer
from rest_framework.decorators import api_view

from datetime import datetime  

from django.db.models import Sum

# ibm
import json
import math
from ibm_watson import LanguageTranslatorV3
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Create your views here.
def addCounter(request):

    count_data = JSONParser().parse(request)
    sirat = count_data['sirat']
    count_data.pop('sirat')

    authenticator_translate = IAMAuthenticator(settings.API_KEY_TRANSLATOR)
    authenticator_tone = IAMAuthenticator(settings.API_KEY_TONE)
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator_translate
    )

    language_translator.set_service_url(settings.URL_TRANSLATOR)
    language_translator.set_disable_ssl_verification(True)

    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator_tone
    )

    tone_analyzer.set_service_url(settings.URL_TONE)
    tone_analyzer.set_disable_ssl_verification(True)

    if not sirat:
        return JsonResponse('fail', status=status.HTTP_200_OK, safe=False)

    translation = language_translator.translate(
        text=sirat,
        model_id='id-en').get_result()

    text = translation['translations'][0]['translation']

    if not text:
        return JsonResponse('fail', status=status.HTTP_200_OK, safe=False)

    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='application/json'
    ).get_result()

    res_arr_tone = tone_analysis['document_tone']['tones']
    # str_tone = ""
    # for t in res_arr_tone:
    #     percent = math.floor(t['score'] * 100)
    #     str_tone += t['tone_name'] + " "+ str(percent) +"% \n"

    # if not str_tone:
    #     return JsonResponse('Tidak dapat menyiratkan', status=status.HTTP_200_OK, safe=False)

    # translation = language_translator.translate(
    #     text=str_tone,
    #     model_id='en-id').get_result()


    isExist = True

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    try:
        count = Counter.objects.get(creation_time=today)
    except Counter.DoesNotExist:
        isExist = False
        count_serializer = CounterSerializer(data=count_data)
        if count_serializer.is_valid():
            count_serializer.save() 
            return JsonResponse(res_arr_tone, status=status.HTTP_200_OK,safe=False) 

    if isExist:
        count_data['count'] = count.count + 1
        count_update_serializer = CounterSerializer(count, data=count_data)
        if count_update_serializer.is_valid():
            count_update_serializer.save()
            return JsonResponse(res_arr_tone, status=status.HTTP_200_OK,safe=False) 
         
    return JsonResponse(count_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):

    # return HttpResponse(str(settings.API_KEY_TRANSLATOR))
    
    count_all = Counter.objects.all()
    count = Counter.objects.aggregate(Sum('count'))

    return render (request, 'index.html',{
        'count':count,
        'count_all':count_all
    })
