from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Review(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    #email = models.EmailField(max_length=250)
    review = models.TextField()
    #desc = models.TextField()
    date = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.review


    
class Booking(models.Model):
    name = models.CharField(max_length=100,null=False)
    email = models.EmailField(null=False)
    phone = models.IntegerField(null=False)
    address = models.TextField(null=False)
    slot = models.CharField(max_length=50)
    type_waste = models.CharField(max_length=100)
    vehicle = models.CharField(max_length=100) 
    
    
    def __str__(self):
        return self.name
    
    
class myuploadfile(models.Model):
    #name = models.CharField(max_length=225)
    f_name = models.CharField(max_length=225)
    myfiles = models.FileField(upload_to="")
    
    def __str__(self):
        return self.f_name
    
    
    
