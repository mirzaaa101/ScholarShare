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
    # use pattern like core_name if you are working for core folder
    path('core/home/', views.core_home, name='core_home'),
    path('core/user/', views.core_user, name='core_user'),
    path('core/update_profile',views.update_profile, name='update_profile' ),
    path('core/create_loan_post',views.create_loan_post, name='create_loan_post'),
    path('core/create_donation_post',views.create_donation_post, name='create_donation_post'),
    path('core/view_post/<int:pk>/', views.view_post, name='view_post'),
    path('logout/', views.logout_user, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)