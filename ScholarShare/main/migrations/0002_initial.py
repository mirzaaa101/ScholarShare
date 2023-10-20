# Generated by Django 4.2.6 on 2023-10-20 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('usertype', models.CharField(max_length=20)),
                ('username', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=8)),
                ('full_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=11)),
                ('profile_photo', models.ImageField(upload_to='Files/profile_photos/')),
                ('uiuid', models.ImageField(upload_to='Files/uiuid_photos/')),
                ('nid', models.ImageField(upload_to='Files/nid_photos/')),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
