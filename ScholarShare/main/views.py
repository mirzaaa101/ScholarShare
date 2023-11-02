from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from.models import NewUser, FAQ
from ScholarShare import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .tokens import generate_token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str


def welcoming_page(request):
    image_filenames = [
        'review1.jpg',
        'review2.jpg',
        'review3.jpg',
        'review4.jpg',
        'review5.jpg',
        'review6.jpg',
    ]
    return render(request, 'welcoming_page.html',{'image_filenames': image_filenames})

def logout_user(request):
    logout(request)
    messages.error(request,"You have been logged out successfully!!")
    return redirect('welcoming_page')

def confirm_registration(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user)
        messages.error(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return render(request,'activation_failed.html')

def register_user(request):
    if request.method == "POST":
        usertype = request.POST['usertype']
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        profile_photo = request.FILES['profile_photo']
        uiuid = request.FILES['uiuid_photo']
        nid = request.FILES['nid_photo']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'The email address is already in use.Please try with another email.')
            return redirect('register')

        if len(password)>8:
            messages.error(request,"Please use 8 characters for your password!!")
            return redirect('register')


        user = User.objects.create_user(username, password=password, is_active = False)
        new_user = NewUser(
            usertype=usertype,
            username = username,
            password = password,
            full_name=full_name,
            phone=phone,
            profile_photo=profile_photo,
            uiuid=uiuid,
            nid=nid,
        )
        new_user.save()
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ ScholarShare Login!!"
        message2 = render_to_string('confirm_login.html',{
            'full_name': full_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [username],
        )
        email.fail_silently = True
        email.send()
        messages.error(request, 'Thank you for signing up. We will send you a confirmation email soon.')
        return redirect('register')
    else:
        return render(request, 'register_user.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username.endswith('uiu.ac.bd'):
            messages.error(request, "You must log in with a valid email address")
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.error(request, "You have been logged in successfully!")
                return redirect('core:home')
            else:
                messages.error(request, 'Sorry, your account is inactive. We will send you a confirmation email soon.')
                return redirect('login')
        else:
            messages.error(request, "Sorry, your email/password is not correct. Please try again.")
            return redirect('login')
    else:
        return render(request, 'login_user.html', {})



def redirect_to_core(request, user):
    return redirect('core:home')

def faqs(request):
    faqs = FAQ.objects.all()
    return render(request,'faqs.html', {'faqs':faqs})