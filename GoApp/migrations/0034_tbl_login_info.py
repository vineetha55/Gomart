# Generated by Django 5.0.3 on 2024-05-16 10:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('GoApp', '0033_tbl_delivery_partner_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_login_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('login_at_date', models.DateField(auto_now_add=True)),
                ('login_at_time', models.TimeField(auto_now_add=True)),
            ],
        ),
    ]
