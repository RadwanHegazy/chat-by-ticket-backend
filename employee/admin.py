from django.contrib import admin
from .models import User, Employee

class adminPanel (admin.ModelAdmin) :
    list_display = ('full_name','email','picture')

admin.site.register(User, adminPanel)

admin.site.register(Employee)