
from django.contrib import admin

# Register your models here.

from .models import MyUser

class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id','name','mobile','email_id','email']
    search_fields = ['mobile']
    
admin.site.register(MyUser, MyUserAdmin)