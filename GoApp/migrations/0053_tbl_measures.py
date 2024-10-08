# Generated by Django 5.0.3 on 2024-07-30 11:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoApp', '0052_alter_tbl_poster1_link_alter_tbl_poster2_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_Measures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_weight', models.CharField(max_length=100, null=True)),
                ('product_measure', models.CharField(max_length=100, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GoApp.tbl_product')),
            ],
        ),
    ]
