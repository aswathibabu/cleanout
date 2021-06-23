from django.contrib import admin
from . models import Booking, Review,myuploadfile

# Register your models here.
admin.site.register(Review)
admin.site.register(Booking)
admin.site.register(myuploadfile)
