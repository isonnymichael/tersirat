from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'homepage'

urlpatterns = [
    path('',views.index, name='index'),
    url(r'^count$', views.addCounter)
]