# Generated by Django 5.0.3 on 2024-04-03 23:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoApp', '0006_rename_vat_amount_tbl_product_tax_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_wishlist',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='tbl_wishlist',
            name='total_price',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='tbl_Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('total_price', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GoApp.tbl_product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GoApp.tbl_signup')),
            ],
        ),
    ]
