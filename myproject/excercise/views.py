from itertools import count
from multiprocessing import context
from django.shortcuts import render
from django.urls import path
from . import views
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
# Create your views here.
# def index(request):
#     template = loader.get_template('myFirst.html')
#     user = request.user
#     context = {
#       'user_details' : user
#     }
#     return HttpResponse(template.render(request,context))
# def capfirst(request):
#   return HttpResponse('''<a href="/index">capitalize first letter</a>''')

def index(request):
  return render(request,'index.html')

def analyze(request):
  djtext = request.POST.get('text','default')
  removepunc = request.POST.get('removepunc','off')
  fullcaps = request.POST.get('fullcaps','off')
  lineremove = request.POST.get('lineremove','off')
  spaceremove = request.POST.get('spaceremove','off')
  charcount = request.POST.get('charcount','off')
  context = {}

  if removepunc=='on':
    punctuations = '''!()-{}[];:'"\,<>_/?@#$&^*%'''
    analyzed = ""
    for char in djtext:
      if char not in punctuations:
        analyzed = analyzed + char
    context = {
      'purpose': 'Removed Punctuations',
      'analyzed_text': analyzed,
    }
    djtext = analyzed
    

  if fullcaps=='on':
    analyzed = ""
    for char in djtext:
        analyzed = analyzed + char.upper()
    context = {
      'purpose': 'Upper Case',
      'analyzed_text': analyzed,
    }
    djtext = analyzed
    

  if lineremove=='on':
    analyzed = ""
    for char in djtext:
      if char!='\n' and char!='\r':
        analyzed = analyzed + char
    context = {
      'purpose': 'New Line Remover',
      'analyzed_text': analyzed,
    }
    djtext = analyzed
    

  if spaceremove=='on':
    analyzed = ""
    for index, char in enumerate(djtext):
      if not(djtext[index]==" " and djtext[index+1]==" "):
        analyzed = analyzed + char
    context = {
      'purpose': 'Extra Space Remover',
      'analyzed_text': analyzed,
    }
    djtext = analyzed
    

  if charcount=='on':
    count = 0
    for char in djtext:
      if char!=" ":
        count = count+1
    
    context = {
      'purpose': 'Char Count',
      'analyzed_text': count,
    }

  if(charcount=='off' and spaceremove=='off' and fullcaps=='off' and lineremove=='off' and removepunc=='off'):
    messages.error(request,'Select any option') 
  
  return render(request,'analyze.html',context)
  
    
    
    

  



