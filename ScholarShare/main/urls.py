from django.urls import path
from . import views

urlpatterns = [
    path('',views.welcoming_page, name='welcoming_page' ),
]
