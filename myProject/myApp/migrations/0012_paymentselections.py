# Generated by Django 4.1.7 on 2023-02-22 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myApp", "0011_delete_video"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentSelections",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Required", max_length=255, verbose_name="name"
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment Selection",
                "verbose_name_plural": "Payment Selections",
            },
        ),
    ]
