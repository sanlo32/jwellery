# Generated by Django 5.0.6 on 2024-07-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0006_billitem_huid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='date',
        ),
        migrations.AlterField(
            model_name='billitem',
            name='gross_weight',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='billitem',
            name='net_weight',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='billitem',
            name='stone_weight',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
    ]
