from typing import Any
from django.db import models

class NewUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    usertype = models.CharField(max_length=20)
    username = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=8)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    profile_photo = models.ImageField(upload_to='Files/profile_photos/')
    uiuid = models.ImageField(upload_to='Files/uiuid_photos/')
    nid = models.ImageField(upload_to='Files/nid_photos/')
    is_active = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.username}-[{self.full_name}]"


class FAQ(models.Model):
    f_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.question}"