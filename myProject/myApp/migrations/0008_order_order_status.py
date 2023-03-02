# Generated by Django 4.1 on 2022-12-14 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myApp", "0007_alter_cartproduct_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_status",
            field=models.CharField(
                choices=[
                    ("Order Received", "Order Received"),
                    ("Order Processing", "Order Processing"),
                    ("On the way", "On the way"),
                    ("Order Completed", "Order Completed"),
                    ("Order Canceled", "Order Canceled"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]