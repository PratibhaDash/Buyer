# Generated by Django 3.2.8 on 2021-11-30 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_productcommission'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='commission',
            field=models.FloatField(default=7.0),
        ),
        migrations.AddField(
            model_name='variant',
            name='payment_percentage',
            field=models.FloatField(default=30.0),
        ),
        migrations.AddField(
            model_name='variant',
            name='price',
            field=models.FloatField(default=30.0),
        ),
        migrations.DeleteModel(
            name='ProductCommission',
        ),
    ]
