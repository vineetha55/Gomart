# Generated by Django 5.0.3 on 2024-04-29 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoApp', '0026_alter_tbl_product_gross_total_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_product',
            name='tax_rate',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
