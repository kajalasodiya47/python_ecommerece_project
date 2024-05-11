from django.contrib import admin
from . models import *
# Register your models here.

# class show_user(admin.ModelAdmin):
#     List_display = ["email","firstname","lastname"]
# admin.site.register(User,show_user)

admin.site.register(User)
admin.site.register(Product)
admin.site.register(wishlsit)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Ajax)