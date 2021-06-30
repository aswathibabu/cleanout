from os import name

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from clean . models import Review
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import PasswordChangeForm,AuthenticationForm
from . models import BookSlot, Booking, Review
from . models import Booking
from . forms import Edit_review, SlotForm
from . forms import Booking_form
from django.views import View
from . models import  myuploadfile
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView

from django.core.mail import send_mail
from django.conf import settings

from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
import stripe




# @csrf_exempt
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#         return JsonResponse(stripe_config, safe=False)
    
    
# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'GET':
#         domain_url = 'http://localhost:8000/'
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try:
#             # Create new Checkout Session for the order
#             # Other optional params include:
#             # [billing_address_collection] - to display billing address details on the page
#             # [customer] - if you have an existing Stripe Customer ID
#             # [payment_intent_data] - capture the payment later
#             # [customer_email] - prefill the email input in the form
#             # For full details see https://stripe.com/docs/api/checkout/sessions/create

#             # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
#             checkout_session = stripe.checkout.Session.create(
#                 success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=domain_url + 'cancelled/',
#                 payment_method_types=['card'],
#                 mode='payment',
#                 line_items=[
#                     {
#                         'name': 'T-shirt',
#                         'quantity': 1,
#                         'currency': 'usd',
#                         'amount': '2000',
#                     }
#                 ]
#             )
#             return JsonResponse({'sessionId': checkout_session['id']})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})    
    
    
    
    


# Create your views here.

def index(request):
    review = Review.objects.all()
    #print(review)
    context ={'reviews':review}
    return render(request,'home.html',context)


def send_files(request):
    if request.method == "POST":
        #user_name = request.POST.get("name")
        file_name = request.POST.get("filename")
        myfile = request.FILES.getlist("uploadfiles")
        
        for f in myfile:
            myuploadfile(f_name=file_name,myfiles=f).save()
            
        print(myfile)
        #return HttpResponse("ok")
        #return render(request,'')
        return redirect('/')


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
    # import pdb
    # pdb.set_trace()
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

#@login_required

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

#@login_required

def booking_form(request):
    form = Booking_form()
    if request.method=='POST':
        form = Booking_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Booking has been successfully...Thank you for using cleanout service...')
            return redirect('/')
    book = Booking.objects.all()
    return render(request,'booking.html',{'form':form, 'bk':book})




# def bookslot_form(request):
#     form = SlotForm()
#     if request.method=='POST':
#         form = SlotForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'Booking has been successfully...Thank you for using cleanout service...')
#             return redirect('/')
#     book = BookSlot.objects.all()
#     return render(request,'slotbook.html',{'form':form, 'bk':book})

def bookslot_form(request):
    return render(request,'slotbook.html')




def delete_booking(request, id):
    if request.method == 'POST':
        book = Booking.objects.get(id=id)
        book.delete()
        return HttpResponseRedirect('/')
    
    
def update_booking(request):
    return render(request,'edit_booking.html', {'id':id})

                
    
''' def delete(request,id):
        review = Review.objects.get(id=id) 
        #print(review) 
        review.delete()
        messages.success(request,"review has been deleted")
        return redirect('/')'''
   

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


# def slotbook(request):
#     return render(request,'slotbook.html')


def order(request):
    return render(request,'slot.html')

def join(request):
    return render(request,'join.html')