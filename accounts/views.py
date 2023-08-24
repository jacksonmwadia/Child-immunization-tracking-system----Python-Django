
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import  send_mail
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from accounts.models import Doctor
from .utils import token_gen
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from decouple import config

from .forms import LoginForm, RegistrationForm
User = get_user_model()

"""for threading function where a user 
is told a function is complete while still loading
"""
import threading

import africastalking

username = "vax"
api_key = config('API_KEY')
africastalking.initialize(username, api_key)



# Create your views here.
# class EmailThread(threading.Thread):
#     def __init__(self, mail):
#         self.mail = mail
#         threading.Thread.__init__(self)
        
#     def run(self):
#         self.mail.send_mail()

        
def LogInView(request, *args, **kwargs):
    next_page = request.GET.get('next')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(email, password)
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if next_page is not None:  
                        return HttpResponseRedirect(next_page)
                    if request.user.is_doctor:
                        return redirect('core:doctor-dashboard')
                    if request.user.is_ministry:
                        return redirect('custom-admin:index')
                    if request.user.is_admin:
                        return redirect('custom-admin:index')
                    if request.user.is_doctor:
                        return redirect('core:doctor-dashboard')
                    return redirect('core:parent-dashboard')
                messages.error(request,"invalid Login! Try again")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            print(form.errors)
            return render(request, 'auth/login.html')
    context = {
        'form': form,
    }
    return render(request, 'auth/login.html', context)

def LogOutView(request, *args, **kwargs):
    logout(request)
    messages.success(request,"You successfully logged out")
    return redirect('core:index')

def RegisterView(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain #gives us the domain
            link = reverse('accounts:activate', 
                            kwargs={
                                'uidb64':uidb64, 
                                'token':token_gen.make_token(user)
                                    })
            activate_url = f"http://{domain+link}"
            
            mail_subject = "Activate your account"

            
            mail_body = f"hi {user.username} click the link below to verify your account\n {activate_url}"
            mail = send_mail (mail_subject, mail_body,'noreply@courses.com',[user.email], fail_silently=False)
            messages.success(request, "Account created, Check your email to activate your account")
            return redirect('accounts:login')
        return render(request, 'auth/register.html', {'form': form})  
    return render(request, 'auth/register.html', {'form': form})

def DoctorRegistration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        license_no = request.POST.get('license_no')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if email == "":
            messages.error(request, "Email is required")
        if phone == "":
            messages.error(request, "phone is required")
        if password1 == "":
            messages.error(request, "Password is required")
        if password2 == "":
            messages.error(request, "Repeat Password is required")
            return redirect('accounts:register-doctor')
        if license_no == "":
            messages.error(request, "License Number is required")
            return redirect('accounts:register-doctor')
        
       
        if User.objects.filter(phone_no=phone).exists():
            messages.error(request, "The Phone Number has already been taken")
        if User.objects.filter(email=email).exists():
            messages.error(request, "The Email has already been taken")
            return redirect('accounts:register-doctor')

        
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        if len(password1)<6:
            messages.error(request,"Password is too short")
            return redirect('accounts:register-doctor') 
            
        if len(license_no)<6:
            messages.error(request,"License Number is too short")
            return redirect('accounts:register-doctor')

        if Doctor.objects.filter(license_no=license_no).exists():
            messages.error(request, "The License Number has already been taken")
            return redirect('accounts:register-doctor')
                
        else:
            user = User.objects.create_user(username=email, 
                                            email=email,
                                            phone_no=phone,
                                            is_doctor=True,
                                            is_parent=False

            )
            user.set_password(password1)
            user.is_active=False
            user.save()

            doctor = Doctor.objects.create(user=user,
                                            license_no=license_no
            )
            doctor.save()               
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain #gives us the domain
            link = reverse('accounts:activate', 
                            kwargs={
                                'uidb64':uidb64, 
                                'token':token_gen.make_token(user)
                                    })
            activate_url = f"http://{domain+link}"
            
            mail_subject = "Activate your account"
            mail_body = f"Hello click the link below to verify your account\n {activate_url}"
            mail = send_mail (mail_subject, mail_body,'noreply@courses.com',[email], fail_silently=False)
            messages.success(request, "Account created, Check your email to activate your account")
            return redirect('accounts:login')
            
    return render(request, 'auth/register-doctor.html', {})

def VerificationView(request,uidb64, token):

    uidb = force_str(urlsafe_base64_decode(uidb64)) or None
    user = User.objects.get(pk=uidb) or None

        
    if user is not  None and token_gen.check_token(user, token):
        user.is_active=True
        user.save()
        messages.info(request, "account activated successfully")  
        return redirect("accounts:login")
    return render(request,'auth/activation_failed.html')


def RequestResetEmail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
    
        user = User.objects.filter(email=email)
    
        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            domain = get_current_site(request).domain #gives us the domain
            link = reverse('accounts:reset-password', 
                            kwargs={
                                'uidb64':uidb64, 
                                'token':PasswordResetTokenGenerator().make_token(user[0])
                                    })
            reset_password_url = f"http://{domain+link}"
            
            mail_subject = "Reset Password"

            
            mail_body = f"hi {user[0].username} click the link below to reset your password\n {reset_password_url}"
            mail = send_mail (mail_subject, mail_body,'noreply@courses.com',[email], fail_silently=False)
            messages.success(request, "Check your Email for the reset link")
            return redirect('accounts:login')
        else:
            messages.error(request, "Sorry, there is no user with that email")
            return redirect('accounts:request-reset-email')

    return render(request, 'auth/reset_email_form.html', {})
  
def ResetPasswordView(request, uidb64, token):
    
    if request.method == 'POST':
        context = {
            'uidb64':uidb64,
            'token':token,
        }
        
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')
        
        if password1 == "":
            messages.error(request, "Password is required")
        if password2 == "":
            messages.error(request, "Repeat Password is required")
            return render(request, 'auth/reset_password.html', context)
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        if len(password1)<6:
            messages.error(request,"Password is too short")
            return render(request, 'auth/reset_password.html', context)
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        if len(password1)<6:
            messages.error(request,"Password is too short")
            return render(request, 'auth/reset_password.html', context)  
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            messages.success(request, "password changed successfully")
            return redirect('accounts:login')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "oops! something went wrong")
            return render(request, 'auth/reset_password.html', context)
        
    context = {
        'uidb64':uidb64, 
        'token':token
        }
        
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.error(request, "Opps, The link has expired")
            return render(request, 'auth/reset_email_form.html')
        
        messages.success(request, "verified")
        return render(request, 'auth/reset_password.html', context)
    except DjangoUnicodeDecodeError as identifier:
        messages.error(request, "oops! something went wrong")
        return render(request, 'auth/reset_email_form.html', context)
