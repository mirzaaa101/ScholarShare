# Generated by Django 4.2.6 on 2023-11-11 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_faq'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='is_active',
        ),
        migrations.AddField(
            model_name='newuser',
            name='userid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
