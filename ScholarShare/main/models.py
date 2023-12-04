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
    confirmation_token = models.CharField(max_length=100, blank=True, null=True)
    userid = models.CharField(max_length=20, unique=True, primary_key=True)
    bio = models.CharField(max_length=200, default="Welcome to my profile! I'm a passionate individual with diverse interests and talents. Join me on my journey and let's explore the world together.")


    def save(self, *args, **kwargs):
        self.userid = self.full_name.split()[0] + self.phone[5:9]
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.username}-[{self.full_name}]"


class FAQ(models.Model):
    f_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.question}"



class About(models.Model):
    dev_img = models.ImageField(upload_to='Files/Teams/')
    dev_name = models.CharField(max_length=100)
    dev_role = models.CharField(max_length=50)
    dev_description = models.CharField(max_length=300)


    def __str__(self):
        return f"{self.dev_name}"

    class Meta:
        verbose_name_plural = 'About'



class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    comment = models.TextField(max_length=300)


    def __str__(self):
        return f"From {self.name}"


class LoanRequest(models.Model):
    loan_postid = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    loan_post = models.CharField(max_length=500)
    loan_amount = models.FloatField(default=0)
    loan_postimage = models.ImageField(upload_to='Files/LoanPost/')
    isactive = models.BooleanField(default=True)
    userid = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    transaction_happen = models.BooleanField(default=False)

    def __str__(self):
        return f"LoanPost {self.loan_postid} by {self.userid}"


class DonationRequest(models.Model):
    donation_postid = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    donation_post = models.CharField(max_length=500)
    donation_amount = models.FloatField(default=0)
    donation_postimage = models.ImageField(upload_to='Files/DonationPost/')
    isactive = models.BooleanField(default=True)
    userid = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    transaction_happen = models.BooleanField(default=False)

    def __str__(self):
        return f"DonationPost {self.donation_postid} by {self.userid}"


class Comment(models.Model):
    commentid = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    posttype = models.CharField(max_length=20)
    postid = models.CharField(max_length=20)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.userid} - {self.comment[:20]}'

class AddBalance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    available_balance = models.FloatField(default=0.00)
    is_first_transaction = models.BooleanField(default=True)

    def __str__(self):
        return f'Balance {self.available_balance} of {self.user.userid}'


class AddDonation(models.Model):
    donation_id = models.AutoField(primary_key=True)
    donated_to = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='donations_received')
    donation_post = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='donations')
    donated_user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='donations_made')
    amount = models.FloatField(default=0.00)
    wish = models.CharField(max_length=200)

    def __str__(self) -> str:
         return f'{self.donated_user.userid} donated {self.amount}'
