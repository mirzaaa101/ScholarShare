# Generated by Django 4.2.6 on 2023-12-04 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddBalance',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('available_balance', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.newuser')),
            ],
        ),
    ]
