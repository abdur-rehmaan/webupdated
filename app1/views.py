from django.shortcuts import render , HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login as django_login, logout
from app1 import views
from .models import *
# Create your views here.
def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1!=password2:
            return HttpResponse("passwords does not match!")
        else:
            myuser=User.objects.create_user(username,email,password1)
            myuser.save()
            return redirect('login')

    return render(request,'signup.html')

def home(request):
    return render(request, 'home.html')
def login(request): 
    if request.user.is_authenticated:
        return redirect ('home' )
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1= request.POST.get('pass')
        user = authenticate(username=username,password=pass1) 
        if user is not None:
            django_login(request,user)
            response = redirect('home') 
            response.set_cookie('username', username)
            return response
        else :
           return HttpResponse("invalid credentials")

    return render(request,'login.html')
def LogoutPage(request):
    logout(request)
    return redirect('login') 

def newarrival(request): 
        products = Product.objects.all()
        context = {'products': products } 
        return render(request,'newarrival.html',context=context)

def categories(request):
    if request.method == "GET":
        return render(request,"categories.html") 
def cart(request):
    if request.user.is_authenticated:
         items = orderItem.objects.all()
         context = {'items': items}
         return render(request,"cart.html",context=context) 
    else:
        return redirect('login')

def checkout(request):
     if request.user.is_authenticated:
        if request.method == 'POST':
            address=request.POST.get('address')
            city= request.POST.get('city')
            state= request.POST.get('state')
            zipcode= request.POST.get('zipcode')
            shipping_details = shipping(
                address=address,
                city=city,
                state=state,
                zipcode=zipcode
            )
            shipping_details.save() 
        items = orderItem.objects.all() 
        context={'item': items }
        return render (request ,"checkout.html" , context )
     else:
         return redirect ("login")
     