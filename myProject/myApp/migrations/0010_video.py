# Generated by Django 4.1 on 2023-01-10 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myApp", "0009_alter_order_total"),
    ]

    operations = [
        migrations.CreateModel(
            name="Video",
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
                ("caption", models.CharField(max_length=100)),
                ("video", models.FileField(upload_to="video/%y")),
            ],
        ),
    ]