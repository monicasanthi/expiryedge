# Generated by Django 5.1.5 on 2025-02-12 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_billing_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing_page',
            name='address',
            field=models.CharField(default='exit', max_length=255),
            preserve_default=False,
        ),
    ]
