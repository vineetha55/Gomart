# Generated by Django 5.0.3 on 2024-06-25 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoApp', '0044_tbl_checkout_created_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_admin_login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
