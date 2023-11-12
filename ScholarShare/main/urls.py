from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.welcoming_page, name='welcoming_page' ),
    path('contact/', views.contact, name='contact'),
    path('register',views.register_user, name='register' ),
    path('confirm/<uidb64>/<token>', views.confirm_registration, name='confirm_registration'),
    path('login',views.login_user, name='login' ),
    path('logout',views.logout_user, name='logout' ),
    path('faqs',views.faqs, name='faqs' ),
    path('about',views.about, name='about' ),
    path('redirect-to-core/', views.redirect_to_core, name='redirect_to_core'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)