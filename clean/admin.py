from django.contrib import admin
from . models import BookSlot, Booking, Review, SlotTime,myuploadfile

# Register your models here.
admin.site.register(Review)
admin.site.register(Booking)
admin.site.register(myuploadfile)
admin.site.register(SlotTime)
admin.site.register(BookSlot)

