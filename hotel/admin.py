from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Hotel)
admin.site.register(hotelBooking)
admin.site.register(hotelImages)
admin.site.register(Amenities)
