from django.contrib import admin
from django.urls import path, include
from django.urls import re_path 
from myApp import views

app_name = 'myApp'

urlpatterns = [
    path('',views.register, name='register'),
    path('register_record/',views.register_record, name='register_record'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('emp/', views.emp, name='emp'),
    path('add/', views.add, name='add'),
    path('add/addrecord/', views.addrecord, name='addrecord'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('update/<int:id>', views.update, name='update'),
    path('update/updaterecord/<int:id>', views.updaterecord, name='updaterecord'),
    path('details/<int:id>',views.details, name='details'),
]  
    
