# Generated by Django 5.0.6 on 2024-06-23 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_remove_bill_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pro_pic',
            field=models.FileField(blank=True, null=True, upload_to='pro_pictures'),
        ),
    ]
