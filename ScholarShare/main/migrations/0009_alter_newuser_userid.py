# Generated by Django 4.2.6 on 2023-11-12 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_newuser_id_alter_newuser_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='userid',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]