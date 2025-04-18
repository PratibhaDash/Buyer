# Generated by Django 3.2.8 on 2021-11-26 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('farm_app', '0001_initial'),
        ('product', '0001_initial'),
        ('buyer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmpurchase',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farm_purchase_category', to='product.category'),
        ),
        migrations.AddField(
            model_name='farmpurchase',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farm_purchase', to='farm_app.farms'),
        ),
        migrations.AddField(
            model_name='farmpurchase',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farm_purchase_product', to='product.product'),
        ),
    ]
