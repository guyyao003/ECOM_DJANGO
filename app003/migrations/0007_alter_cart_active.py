# Generated by Django 5.0.3 on 2024-04-05 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app003', '0006_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
