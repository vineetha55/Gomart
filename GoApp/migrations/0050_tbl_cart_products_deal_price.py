# Generated by Django 5.0.3 on 2024-07-04 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoApp', '0049_tbl_signup_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_cart_products',
            name='deal_price',
            field=models.FloatField(null=True),
        ),
    ]