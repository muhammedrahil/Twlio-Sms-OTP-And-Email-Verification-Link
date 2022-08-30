from django.contrib import admin
from .models import User

from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserAccounts(UserAdmin):
    list_display = ('email','phone_no','first_name','last_name','is_active')
    filter_horizontal=[]
    list_filter=[]
    fieldsets = []
    search_fields=['email']
    ordering =()
    list_display_links =['email','first_name']
    list_filter =['email']

admin.site.register(User,UserAccounts)