# Generated by Django 4.1 on 2022-12-14 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myApp", "0008_order_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="total",
            field=models.PositiveIntegerField(null=True),
        ),
    ]
