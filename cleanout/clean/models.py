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
    
