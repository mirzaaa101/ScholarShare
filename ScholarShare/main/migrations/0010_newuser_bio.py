# Generated by Django 4.2.6 on 2023-11-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_newuser_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='bio',
            field=models.CharField(default='', max_length=100),
        ),
    ]