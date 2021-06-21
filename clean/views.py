from clean.models import Review
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import PasswordChangeForm
from . models import Review
#from . models import Booking
from . forms import Edit_review
from . forms import Booking_form
from django.views import View

# Create your views here.

def index(request):
    review = Review.objects.all()
    #print(review)
    context ={'reviews':review}
    return render(request,'home.html',context)

def user_register(request):
    if request.method=='POST':
        fname = request.POST.get('firstname')
        lname =request.POST.get('lastname')
        uname =request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 =request.POST.get('pass2')
        
        if pass1!=pass2:
            messages.warning(request,'Password does not match')
            return redirect('register')
        elif User.objects.filter(username=uname).exists():
            messages.warning(request,'username already taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.warning(request,'email already taken')
            return redirect('register')
        else:        
            #print(fname,lname,uname,email,pass1,pass2)
            user = User.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=pass1)
            user.save()
            messages.success(request,'User has been registered successfully')
            return redirect('login')
        
    return render(request,'register.html')

def user_login(request):
    if request.method=="POST":
        username =request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request,'Invalid credentials')
            return redirect('login') 
               
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')


def post_review(request):
    if request.method=="POST":
        name = request.POST.get('name')
        review = request.POST.get('review')
        #print(name,review)
        review = Review(name=name,review=review,user_id=request.user)
        review.save()
        messages.success(request,'review has been posted successfully')
        return redirect('/')
        
    return render(request,'review.html')


def review_details(request,id):
    review = Review.objects.get(id=id) 
    #print(review) 
    context = {'review':review}  
    return render(request,'review_details.html',context)

def delete(request,id):
    review = Review.objects.get(id=id) 
    #print(review) 
    review.delete()
    messages.success(request,"review has been deleted")
    return redirect('/')

def edit(request,id):
    review = Review.objects.get(id=id) 
    #print(review) 
    editreview = Edit_review(instance=review)
    if request.method=='POST':
        form = Edit_review(request.POST,instance=review)
        if form.is_valid():
            form.save()
            messages.success(request,'review has been updated')
            return redirect('/')
    return render(request,'edit_review.html',{'edit_review':editreview})

def booking_form(request):
    form = Booking_form()
    if request.method=='POST':
        form = Booking_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Booking has been successfully...Thank you for using cleanout service...')
            return redirect('/')
    return render(request,'booking.html',{'form':form})


def change_password(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            #update_session_auth_hash(request,user)
            messages.success(request,'Your password has been changed')
            return redirect('/')
        else:
            messages.warning(request,'Error')
            return redirect('change_password')
    else:    
        form = PasswordChangeForm(request.user)
        return render(request,'change_password.html',{'PasswordChangeForm':form})
    
    
    
    # other option ...it does not contain errors
    '''if request.method=='POST':
        newpass = request.POST.get('newpassword')
        u = User.objects.get(username=request.user.username)
        u.set_password(newpass)
        u.save()
        messages.success(request,'Password has been changed')
        return redirect('/')'''
        