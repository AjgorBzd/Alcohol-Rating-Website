# Generated by Django 4.1.3 on 2023-01-22 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0014_alcohol_alcohol_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="alcohol",
            name="verified",
            field=models.BooleanField(default=False),
        ),
    ]
