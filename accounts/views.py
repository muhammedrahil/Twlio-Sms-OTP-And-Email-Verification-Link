import imp
from .models import User
from django.shortcuts import render,redirect
from .forms import UserForm,LoginUser
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse,Http404


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# register


from .verify import send_otp,verify_otp


def user_login(request,*arg,**kwrgs):
    if request.method == 'POST':
        choice=request.POST['choice']
        form = UserForm(request.POST,None)
        if form.is_valid():
            email=form.cleaned_data['email']
            phone_no=form.cleaned_data['phone_no']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            password=form.cleaned_data['password']
            user=User.objects.create_user(email=email,phone_no=phone_no,first_name=first_name,last_name=last_name,password=password)
            user.save()
            if choice == 'email' :
                current_site = get_current_site(request)
                mail_subject = "Please active your account"
                massage = render_to_string('accounts/verification.html',{
                    'user':user,
                    'domain'  : current_site,
                    # user pk encode 
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    # user token genarete
                    'token': default_token_generator.make_token(user),
                })
                to_email=email
                send_email = EmailMessage(mail_subject,massage,to=[to_email])
                send_email.send()
                return redirect('accounts:login')
            else:
                request.session['uid']=user.pk
                request.session['phone_no']=phone_no
                print("mobile: ",request.session['phone_no'],request.session['uid'])
                send_otp(phone_no)
                return redirect('accounts:verify')
    else:   
        form=UserForm()
    return render(request,'accounts/login.html',{'form':form})




def verify_code(request):
    if  request.method == 'POST':
        otp_check = request.POST.get('otp')
        verify=verify_otp(request.session['phone_no'],otp_check)

        if  verify:
            messages.success(request,'account has created successfuly please login now') 
            user=User.objects.get(pk=request.session['uid'])
            user.is_active = True
            user.save()
            messages.success(request,'Registration Successful')
            return redirect('accounts:login')
        
        else:
            messages.error(request,'invalid otp recheck')
            return redirect ('accounts:verify_code')
        
    return render(request,'accounts/verify.html')

# login 
def reg(request,*arg,**kwrgs):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('core:all_products')
        else:
            messages.error(request,'sorry not work')
            return redirect('accounts:reg')
    form=LoginUser()
    return render(request,'accounts/reg.html',{'form':form})




def user_logout(request,*arg,**kwrgs):
    logout(request)
    return redirect('accounts:login')
    



def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        return redirect('core:all_products')
    else:
        return redirect('accounts:login')
        
    