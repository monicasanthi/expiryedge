# Generated by Django 4.0.7 on 2025-01-29 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_issue'),
    ]

    operations = [
        migrations.CreateModel(
            name='billing_page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phoneno', models.CharField(max_length=255)),
                ('transactionid', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='productdetails',
            name='mrp',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='productdetails',
            name='price',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
