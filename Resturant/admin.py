from django.contrib import admin
from .models import Menu,Category,Cart,Booking,BookingItem
# Register your models here.
admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(Cart)
admin.site.register(Booking)
admin.site.register(BookingItem)
