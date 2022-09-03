from audioop import reverse
from itertools import count
from multiprocessing import context
from pickle import GET
from re import U, template
from tkinter import ON
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from myApp.models import MyApp
from myApp import views
from django.contrib import messages
from django.contrib.auth.models import User, auth


# def index(request):
#   return HttpResponse("Hello World!")

def emp(request):
  if request.method == 'GET':
    if request.user.is_superuser:
      myapps = MyApp.objects.all()
      user_list = User.objects.filter(is_superuser=False)
      template = loader.get_template('emp.html')
      context = {
          'myapps':myapps,
          'user_list':user_list,
      }
      return HttpResponse(template.render(context, request))

    else:
      myapps = MyApp.objects.filter(user=request.user)
      template = loader.get_template('emp.html')
      context = {
          'myapps':myapps,
      }
      return HttpResponse(template.render(context, request))

  else:
    user_list = User.objects.filter(is_superuser=False)
    template = loader.get_template('emp.html')
    u = request.POST['users']
    d = request.POST['date']

    if u and d:
      myapps = MyApp.objects.filter(user=u, date__date=d)

    elif u:
      myapps = MyApp.objects.filter(user=u)

    elif d:
      myapps = MyApp.objects.filter(date__date=d)

    else:
      messages.error(request,'Select Some Filter')
      return render(request,'emp.html')

    # print('user is =====',u)
    # print('user type =====',type(u))
    # by default form date is string type
    # for i in user_list:
    #   print('user type in loop =====',type(i.id) )

    #   if int(u) == i.id:
    #     print('select user is ==',u)
    #   else:
    #     print('not selected ===',i.id)

    context = {
      'myapps':myapps,
      'user_list':user_list,
      'user_id': int(u),
      'sdate':d,
    }
    print('res ====',context)
    return HttpResponse(template.render(context,request))
    
  
def add(request):
  template = loader.get_template('add.html')
  return HttpResponse(template.render({}, request))


def addrecord(request):
  user = request.user
  x = request.POST['first']
  y = request.POST['last']
  z = request.POST['age']
  w = request.POST['qualification']
  c = request.POST['college']
  g = request.POST['city']
  employee = MyApp(user=user, firstname=x, lastname=y, age=z, qualification=w, college=c, city=g)
  employee.save()
  return HttpResponseRedirect(reverse('emp'))

def delete(request, id):
  employee = MyApp.objects.get(id=id)
  employee.delete()
  return HttpResponseRedirect(reverse('emp'))

def update(request, id):
  employee = MyApp.objects.get(id=id)
  template = loader.get_template('update.html')
  context = {
    'employee': employee,
  }
  return HttpResponse(template.render(context, request))

def updaterecord(request, id):
  first = request.POST['first']
  last = request.POST['last']
  age = request.POST['age']
  qualification = request.POST['qualification']
  college = request.POST['college']
  city = request.POST['city']
  date = request.POST['date']
  employee = MyApp.objects.get(id=id)
  employee.firstname = first
  employee.lastname = last
  employee.age = age
  employee.qualification = qualification
  employee.college = college
  employee.city = city
  employee.date = date
  employee.save()
  messages.success(request, 'Your data has been updated successfully!')
  return HttpResponseRedirect(reverse('emp'))

def details(request, id):
  employee = MyApp.objects.get(id=id)
  context = {
    'employee':employee
  }
  template = loader.get_template('details.html')
  return HttpResponse(template.render(context, request))


def register(request):
  template = loader.get_template('register.html')
  return HttpResponse(template.render({}, request))


def register_record(request):
  user = request.POST['username']
  email = request.POST['email']
  password = request.POST['password']
  confirmpassword = request.POST['confirm_password']

  if password == confirmpassword:
    try:
        user = User.objects.get(username=user)
        messages.error(request,'Username Allready Taken!! Try diffrent Username')
        return render(request,'register.html') 

    except User.DoesNotExist:

        try:
            User.objects.get(email=email)
            messages.error(request,'"Email is Allready registered !! Try diffrent Email')
            return render(request,'register.html')
        except User.DoesNotExist:
            userobj = User.objects.create(username=user,email=email,password=password)
            userobj.set_password(password) #save encrypted password in table use ths method
            userobj.save()
            auth.login(request, userobj)  #login after register successful
            messages.success(request,'User Registered Successfully')                          
            #return render(request,'emp.html')    #redirect on any page after login  
            return redirect("/emp")    
  else:
    messages.error(request, 'password does not match')
    return render(request,'register.html')


def login(request):
  if request.method == 'GET':
    template = loader.get_template('login.html')
    return HttpResponse(template.render({},request))
  else:
    un = request.POST['username']
    pd = request.POST['password']

    user = auth.authenticate(request,username=un,password=pd) #authenticate user with this username and password
    if user:
      auth.login(request, user)  # login user
      messages.success(request,'Login successfully')
      #return render(request,'emp.html') 
      return redirect("/emp")
    else:
      try:
        user = User.objects.get(username=un)
        messages.error(request,'password invalid')
        return render(request,'login.html')
      except:
        messages.error(request,'username invalid')
        return render(request,'login.html')

def logout(request):
    # user = request.user (get login user)
    auth.logout(request)
    #return render(request,'login.html')
    return redirect("/login")

def forget_password(request):
  if request.method == 'GET':
    exist = False
    template = loader.get_template('forget_password.html')
    return HttpResponse(template.render({'exist':exist},request))
  else:
    un = request.POST['username']
    try:
      user = User.objects.get(username=un)
      context = {
        'user':user,
      }
      messages.success(request,'Username Exist')
      return render(request,"forget_password.html",context)
    except:
      messages.error(request,'Username not exist')
      return render(request,"forget_password.html")

def change_password(request):
  u = request.POST['uname']
  p = request.POST['password']
  cp = request.POST['confirm_password']

  if p == cp:
    user_data = User.objects.get(username=u)
    user_data.set_password(p)
    user_data.save()
    messages.success(request,'Password updated')
    return render(request,"login.html")
  else:
    messages.error(request,'Both Password are not matching')
    return render(request,"forget_password.html")




  
    

    







        
      
        



      
           

      
      
    



























# def index(request):
#     myapps = MyApp.objects.all().values()
#     output =''
#     for i in myapps:
#         output+=i['firstname']
#     return HttpResponse(output)

# def index(request):
#     students = [
#         {"name": "Sonu","age":25},
#         {"name": "Rohan", "age":23},
#         {"name": "Ravi", "age":20},
#         {"name": "Nitin", "age":21},
#         {"name": "Nidhi", "age":22}
#     ]
    # for dict in students:
    #    print(dict['name']+" and "+str(dict['age']))
    
    # for dict in students:
    #     for i,j in dict.items():
    #       print(i,j)
           

    # return render(request,'index.html',{'students':students})
    

