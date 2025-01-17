# Generated by Django 5.0.1 on 2025-01-11 21:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="telegram_id",
        ),
        migrations.AddField(
            model_name="user",
            name="birth_date",
            field=models.DateField(
                blank=True,
                db_comment="User's date of birth",
                null=True,
                verbose_name="Birth date",
            ),
        ),
        migrations.CreateModel(
            name="UserSocial",
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
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_comment="Creation date and time",
                        verbose_name="Creation date and time",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_comment="Update date and time",
                        verbose_name="Update date and time",
                    ),
                ),
                (
                    "social_type",
                    models.CharField(
                        choices=[("TELEGRAM", "Telegram"), ("WHATSAPP", "WhatsApp")],
                        db_comment="Social type",
                        max_length=50,
                        verbose_name="Social type",
                    ),
                ),
                (
                    "social_user_id",
                    models.CharField(
                        blank=True,
                        db_comment="Social id",
                        max_length=50,
                        null=True,
                        verbose_name="Telegram id",
                    ),
                ),
                (
                    "social_username",
                    models.CharField(
                        blank=True,
                        db_comment="Social username",
                        max_length=255,
                        null=True,
                        verbose_name="Username",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="socials",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "User social",
                "verbose_name_plural": "User socials",
                "db_table": "jw_user_social",
            },
        ),
        migrations.AddConstraint(
            model_name="usersocial",
            constraint=models.UniqueConstraint(
                condition=models.Q(("social_user_id", None), _negated=True),
                fields=("social_type", "social_user_id"),
                name="unique_social_user_id",
            ),
        ),
        migrations.AddConstraint(
            model_name="usersocial",
            constraint=models.UniqueConstraint(
                condition=models.Q(("social_username", None), _negated=True),
                fields=("social_type", "social_username"),
                name="unique_social_username",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="usersocial",
            unique_together={("social_type", "user")},
        ),
    ]
