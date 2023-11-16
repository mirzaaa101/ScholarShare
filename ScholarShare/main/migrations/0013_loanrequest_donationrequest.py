# Generated by Django 4.2.6 on 2023-11-16 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_newuser_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanRequest',
            fields=[
                ('loan_postid', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('loan_post', models.CharField(max_length=500)),
                ('loan_amount', models.FloatField(default=0)),
                ('loan_postimage', models.ImageField(upload_to='Files/LoanPost/')),
                ('isactive', models.BooleanField(default=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.newuser')),
            ],
        ),
        migrations.CreateModel(
            name='DonationRequest',
            fields=[
                ('donation_postid', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('donation_post', models.CharField(max_length=500)),
                ('donation_amount', models.FloatField(default=0)),
                ('donation_postimage', models.ImageField(upload_to='Files/DonationPost/')),
                ('isactive', models.BooleanField(default=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.newuser')),
            ],
        ),
    ]