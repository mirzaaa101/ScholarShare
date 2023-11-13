from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from.models import NewUser, FAQ, About, Message
from ScholarShare import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .tokens import generate_token
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
        bio = request.POST['bio']
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
            full_name = full_name,
            phone=phone,
            profile_photo=profile_photo,
            uiuid=uiuid,
            nid=nid,
            bio = bio,
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
                return redirect('core_home')
            else:
                messages.error(request, 'Sorry, your account is inactive. We will send you a confirmation email soon.')
                return redirect('login')
        else:
            messages.error(request, "Sorry, your email/password is not correct. Please try again.")
            return redirect('login')
    else:
        return render(request, 'login_user.html', {})

def user_exists(view_func):
    def _wrapped_view(request, *args, **kwargs):
        username = request.user.username
        try:
            user = NewUser.objects.get(username=username)
        except NewUser.DoesNotExist:
            user = None
            messages.error(request, "You have been logged out successfully!")
            return redirect('welcoming_page')
        return view_func(request, user=user, *args, **kwargs)

    return _wrapped_view

def faqs(request):
    faqs = FAQ.objects.all()
    return render(request,'faqs.html', {'faqs':faqs})

def about(request):
    devs = About.objects.all()
    return render(request,'about.html', {'devs':devs})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        messages.error(request, "Thank you for contacting us, we will contact you soon if required!")
        Message.objects.create(name=name, email=email, comment=comment)
        subject = "ScholarShare"
        message = f"Dear {name},\n\nThank you for contacting us! We have received your message and will get back to you as soon as possible.\n\nBest regards,\nTeamScrum"
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        send_mail(subject, message, from_email, to_email, fail_silently=True)
        return redirect('welcoming_page')
    else:
        return redirect('welcoming_page')


# Please start writing from here for main functionality


@user_exists
def core_home(request, user):
    if not request.user.is_authenticated:
        logout(request)
        return redirect('welcoming_page')

    return render(request, 'core/home.html', {'user': user})



@user_exists
def core_user(request, user):
    return render(request, 'core/user.html', {'user': user})


def update_profile(request):
    if request.method == 'POST':
        new_bio = request.POST.get('bio')
        new_profile_photo = request.FILES.get('profile_photo')

        username = request.user.username
        new_user = NewUser.objects.get(username=username)
        new_user.bio = new_bio
        if new_profile_photo:
            new_user.profile_photo = new_profile_photo
        new_user.save()

        messages.error(request, 'Profile updated successfully!')
        return redirect('core_user')
    return render(request, 'core/user.html')


def logout_user(request):
    logout(request)
    messages.error(request, "You have been logged out successfully!")
    return redirect('welcoming_page')