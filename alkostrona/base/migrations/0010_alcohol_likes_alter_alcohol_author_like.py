# Generated by Django 4.1.3 on 2023-01-17 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("base", "0009_profile_nickname_alter_profile_profile_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="alcohol",
            name="likes",
            field=models.ManyToManyField(
                blank=True,
                default=None,
                related_name="likes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="alcohol",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Like",
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
                    "value",
                    models.CharField(
                        choices=[("Like", "Like"), ("Dislike", "Dislike")],
                        default="Like",
                        max_length=10,
                    ),
                ),
                (
                    "alcohol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="base.alcohol"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]