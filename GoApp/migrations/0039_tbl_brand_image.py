# Generated by Django 5.0.3 on 2024-06-06 04:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('GoApp', '0038_tbl_poster1_tbl_poster2_tbl_poster3_tbl_poster4_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_brand',
            name='image',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
