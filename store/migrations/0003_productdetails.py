# Generated by Django 4.0.7 on 2025-01-20 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_registration_usertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='productdetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staffID', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('expiry_date', models.CharField(max_length=255)),
                ('product_id', models.CharField(max_length=255)),
                ('quantity', models.CharField(max_length=255)),
                ('notes', models.CharField(max_length=255)),
            ],
        ),
    ]
