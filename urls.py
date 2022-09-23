from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns =[
    
     path("monitor",views.monitor,name='monitor'),
     path("",views.notice1,name='notice'),
     path("two4",views.two4,name='two4'),
     path("two5",views.two5,name='two5')
     

     
     #path("changes",views.changes,name='changes')
     
]