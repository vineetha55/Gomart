# Generated by Django 5.0.3 on 2024-06-05 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoApp', '0037_tbl_deals'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_poster1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='media')),
                ('subtitle', models.CharField(max_length=100, null=True)),
                ('heading', models.CharField(max_length=100, null=True)),
                ('heading2', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_poster2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='media')),
                ('subtitle', models.CharField(max_length=100, null=True)),
                ('heading', models.CharField(max_length=100, null=True)),
                ('heading2', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_poster3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='media')),
                ('subtitle', models.CharField(max_length=100, null=True)),
                ('heading', models.CharField(max_length=100, null=True)),
                ('heading2', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_poster4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtitle', models.CharField(max_length=100, null=True)),
                ('heading', models.CharField(max_length=100, null=True)),
                ('heading2', models.CharField(max_length=500, null=True)),
                ('sentence', models.CharField(max_length=600, null=True)),
                ('image', models.ImageField(null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_poster5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='media')),
                ('subtitle', models.CharField(max_length=100, null=True)),
                ('heading', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_poster6',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_poster7',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='media')),
                ('title', models.CharField(max_length=100, null=True)),
                ('subtitle', models.CharField(max_length=100, null=True)),
                ('subtitle2', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
