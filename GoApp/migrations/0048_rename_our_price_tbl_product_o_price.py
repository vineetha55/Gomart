# Generated by Django 5.0.3 on 2024-06-27 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GoApp', '0047_tbl_site_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tbl_product',
            old_name='our_price',
            new_name='o_price',
        ),
    ]
