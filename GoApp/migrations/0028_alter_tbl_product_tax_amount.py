# Generated by Django 5.0.3 on 2024-04-29 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoApp', '0027_alter_tbl_product_tax_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_product',
            name='tax_amount',
            field=models.FloatField(null=True),
        ),
    ]
