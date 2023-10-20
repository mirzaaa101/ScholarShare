from django.urls import path
from . import views

urlpatterns = [
    path('',views.welcoming_page, name='welcoming_page' ),
    path('register',views.register_user, name='register' ),
    path('confirm/<uidb64>/<token>', views.confirm_registration, name='confirm_registration'),
    path('login',views.login_user, name='login' ),
    path('logout',views.logout_user, name='logout' ),
]
