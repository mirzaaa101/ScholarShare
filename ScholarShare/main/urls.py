from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import view_post


urlpatterns = [
    path('',views.welcoming_page, name='welcoming_page' ),
    path('contact/', views.contact, name='contact'),
    path('register',views.register_user, name='register' ),
    path('confirm/<uidb64>/<token>', views.confirm_registration, name='confirm_registration'),
    path('login',views.login_user, name='login' ),
    path('logout',views.logout_user, name='logout' ),
    path('faqs',views.faqs, name='faqs' ),
    path('about',views.about, name='about' ),
    # Core folder url pattern starts from here
    path('core/home/', views.core_home, name='core_home'),
    path('core/user/', views.core_user, name='core_user'),
    path('statistics/', views.core_statistics, name='core_statistics'),
    path('core/update_profile',views.update_profile, name='update_profile' ),
    path('core/create_loan_post',views.create_loan_post, name='create_loan_post'),
    path('core/create_donation_post',views.create_donation_post, name='create_donation_post'),
    path('core/view_post/<int:pk>/', views.view_post, name='view_post'),
    path('core/view_laon_post/<int:pk>/', views.view_loan_post, name='view_loan_post'),
    path('core/view_donation_post/<int:pk>/', views.view_donation_post, name='view_donation_post'),
    path('delete_loan_post/<int:pk>/', views.delete_loan_post, name='delete_loan_post'),
    path('update_loan_post/<int:pk>/', views.update_loan_post, name='update_loan_post'),
    path('delete_donation_post/<int:pk>/', views.delete_donation_post, name='delete_donation_post'),
    path('update_donation_post/<int:pk>/', views.update_donation_post, name='update_donation_post'),
    path('core/send_donation',views.send_donation, name='send_donation' ),
    path('core/report',views.report, name='report' ),
    path('logout/', views.logout_user, name='logout'),
    path('delete_profile/<str:userid>/<str:username>/', views.delete_profile, name='delete_profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)