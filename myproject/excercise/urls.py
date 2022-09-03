from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from excercise import views 
#from excercise import views as ev (import view as alias)
#from excercise import removepunc (import module directly)

app_name = 'excercise'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('analyze/', views.analyze, name='analyze')
    #path('removepunc/', removepunc),
    #path('removepunc/', ev.removepunc, name='removepunc'),
    # path('removepunc/', views.removepunc, name='removepunc'),
    # path('capitalizefirst/', views.capfirst, name='capfirst'),
    # path('spaceremove/', views.spaceremove, name='spaceremove'),
    # path('charcount/', views.charcount, name='charcount'),
]