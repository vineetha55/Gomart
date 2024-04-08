# Generated by Django 5.0.3 on 2024-04-08 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoApp', '0009_remove_tbl_signup_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_cart',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='tbl_cart',
            name='product',
        ),
        migrations.RemoveField(
            model_name='tbl_cart',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='tbl_cart',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='tbl_cart',
            name='updated_at',
        ),
        migrations.CreateModel(
            name='tbl_Cart_Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('total_price', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GoApp.tbl_cart')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GoApp.tbl_product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GoApp.tbl_signup')),
            ],
        ),
    ]
