# Generated by Django 5.0.3 on 2024-04-08 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GoApp', '0008_tbl_signup_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_signup',
            name='username',
        ),
    ]
