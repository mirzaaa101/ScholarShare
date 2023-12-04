from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from.models import NewUser, FAQ, About, Message,LoanRequest, DonationRequest, Comment, AddBalance
from ScholarShare import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .tokens import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from itertools import chain
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test



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

        if len(phone)>11:
            messages.error(request,"Please use valid phone number!!")
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
    loan_post = LoanRequest.objects.all()
    donation_post = DonationRequest.objects.all()
    all_posts = sorted(
        chain(loan_post, donation_post),
        key=lambda post: post.created_at,
        reverse=True
    )

    for post in all_posts:
        time_difference = timezone.now() - post.created_at
        minutes_since_creation = int(time_difference.total_seconds() / 60)

        if minutes_since_creation < 60:
            post.time_since_creation = f"{minutes_since_creation} minutes ago"
        elif minutes_since_creation < 1440:
            hours_since_creation = minutes_since_creation // 60
            post.time_since_creation = f"{hours_since_creation} hours ago"
        else:
            days_since_creation = minutes_since_creation // 1440
            post.time_since_creation = f"{days_since_creation} days ago"

    if not request.user.is_authenticated:
        logout(request)
        return redirect('welcoming_page')

    return render(request, 'core/home.html', {'user': user, 'all_posts': all_posts})


@user_exists
def core_user(request, user):
    loan_post = LoanRequest.objects.all().order_by('-created_at')
    donation_post = DonationRequest.objects.all().order_by('-created_at')
    return render(request, 'core/user.html', {'user': user, 'loan_post': loan_post, 'donation_post': donation_post})


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


@user_exists
def create_loan_post(request, user):
    if request.method == 'POST':
        post_content = request.POST.get('post')
        amount = request.POST.get('amount')
        post_image = request.FILES.get('post_image')

        if post_content and amount:
            loan_post = LoanRequest.objects.create(
                loan_post=post_content,
                loan_amount=amount,
                loan_postimage=post_image,
                userid=user
            )
            loan_post.save()
            messages.error(request, "Loan post created successfully!")
            return redirect('core_home')
        else:
            messages.error(request, "Error creating loan post. Please fill in all required fields.")
            return redirect('core_home')

    return redirect('core_home')


@user_exists
def create_donation_post(request, user):
    if request.method == 'POST':
        post_content = request.POST.get('post')
        amount = request.POST.get('amount')
        post_image = request.FILES.get('post_image')
        if post_content and amount:
            donation_post = DonationRequest.objects.create(
                donation_post=post_content,
                donation_amount=amount,
                donation_postimage=post_image,
                userid=user
            )
            donation_post.save()
            messages.error(request, "Donation post created successfully!")
            return redirect('core_home')
        else:
            messages.error(request, "Error creating donation post. Please fill in all required fields.")
            return redirect('core_home')
    else:
        return redirect('core_home')




def view_loan_post(request, user, template_name, post, comments):
    return render(request, template_name, {'user': user, 'post': post, 'comments': comments})



def view_donation_post(request, user, template_name, post, comments):
    print(comments)
    return render(request, template_name, {'user': user, 'post': post, 'comments': comments})


@user_exists
def view_post(request, user, pk):
    user_type = request.GET.get('type', '')
    template_name = "#"
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '')
        post_type = request.POST.get('post_type', '')
        post_id = request.POST.get('post_id', '')
        user_id = request.POST.get('user_id', '')

        user = get_object_or_404(NewUser, userid=user_id)
        new_comment = Comment(
            comment=comment_text,
            posttype=post_type,
            postid=post_id,
            user=user,
        )
        new_comment.save()
        messages.error(request, 'Thanks for your comment!')

    comments = Comment.objects.all()
    if user_type == 'Individual':
        post = get_object_or_404(LoanRequest, pk=pk)
        template_name = 'core/view_loan_post.html'
        return view_loan_post(request, user, template_name, post,comments)


    else:
        post = get_object_or_404(DonationRequest, pk=pk)
        template_name = 'core/view_donation_post.html'
        return view_donation_post(request, user, template_name, post,comments)




def delete_loan_post(request, pk):
    loan_post = get_object_or_404(LoanRequest, pk=pk)

    if not loan_post.transaction_happen:
        loan_post.delete()
        messages.error(request, "Post deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this post.")

    return redirect('core_user')


def update_loan_post(request, pk):
    loan_post_reuest = get_object_or_404(LoanRequest, pk=pk)

    if request.method == 'POST' and not loan_post_reuest.transaction_happen:
        new_post = request.POST.get('loan_post')
        new_amount = request.POST.get('loan_amount')
        loan_post_reuest.loan_post = new_post
        loan_post_reuest.loan_amount = new_amount
        loan_post_reuest.save()

        messages.error(request, 'Post updated successfully!')
        return redirect('core_user')
    else:
     messages.error(request, "You don't have permission to update this post.")
     return render(request, 'core/home.html')


def delete_donation_post(request, pk):
    donation_post = get_object_or_404(DonationRequest, pk=pk)

    if not donation_post.transaction_happen:
        donation_post.delete()
        messages.error(request, "Post deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this post.")

    return redirect('core_user')


def update_donation_post(request, pk):
    donation_post_reuest = get_object_or_404(DonationRequest, pk=pk)

    if request.method == 'POST' and not donation_post_reuest.transaction_happen:
        new_post = request.POST.get('donation_post')
        new_amount = request.POST.get('donation_amount')
        donation_post_reuest.donation_post = new_post
        donation_post_reuest.donation_amount = new_amount
        donation_post_reuest.save()

        messages.error(request, 'Post updated successfully!')
        return redirect('core_user')
    else:
     messages.error(request, "You don't have permission to update this post.")
     return render(request, 'core/core_user.html')


def create_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '')
        post_type = request.POST.get('post_type', '')
        post_id = request.POST.get('post_id', '')
        user_id = request.POST.get('user_id', '')

        user = get_object_or_404(NewUser, userid=user_id)
        new_comment = Comment(
            comment=comment_text,
            posttype=post_type,
            postid=post_id,
            user=user,
        )
        new_comment.save()
        messages.error(request, 'Thanks for the comment!')
        return redirect('core_home')
    return render(request, 'core/core_home.html')

@user_exists
def core_statistics(request, user):
    if request.method == 'POST':
        phone = float(request.POST.get('phone'))
        amount = float(request.POST.get('amount', 0))
        add_balance, created = AddBalance.objects.get_or_create(user=user, is_first_transaction=True)

        if not created:
            add_balance.available_balance += amount
            add_balance.is_first_transaction = False
        else:
            add_balance.available_balance = amount

        add_balance.save()
        messages.error(request, f"Balance Added Successfully From the Number {phone} !!")
    available_balance = AddBalance.objects.all()
    return render(request, 'core/statistics.html', {'user': user,'available_balance':available_balance})

def logout_user(request):
    logout(request)
    messages.error(request, "You have been logged out successfully!")
    return redirect('welcoming_page')


def delete_profile(request, userid, username):
    userid = get_object_or_404(NewUser, userid=userid)
    username = get_object_or_404(User,username=username)
    donation_posts = DonationRequest.objects.filter(userid=userid, transaction_happen=True)
    loan_posts = LoanRequest.objects.filter(userid=userid, transaction_happen=True)

    if donation_posts.exists() or loan_posts.exists():
        messages.error(request, "You cannot delete your profile because of existing transactions.")
    else:
        username.delete()
        userid.delete()
        logout(request)
        messages.error(request, "Your profile has been deleted successfully. You have been logged out.")

    return redirect('welcoming_page')