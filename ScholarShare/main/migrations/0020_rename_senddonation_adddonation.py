# Generated by Django 4.2.6 on 2023-12-04 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_senddonation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SendDonation',
            new_name='AddDonation',
        ),
    ]