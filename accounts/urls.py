from django.urls import path
from . import views as v

app_name = 'accounts' 

urlpatterns = [
    
    path('',v.user_login,name='login'),
    path('reg',v.reg,name='reg'),
     path('logout',v.user_logout,name='logout'),
     path('verify/', v.verify_code ,name='verify'), 
     path('activate/<uidb64>/<token>',v.activate,name='activate'),
     
]