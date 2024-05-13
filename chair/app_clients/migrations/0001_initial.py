# Generated by Django 5.0.1 on 2024-02-28 19:57

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "guid",
                    models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
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
                    "phone",
                    models.CharField(
                        db_comment="Phone number without country code",
                        max_length=10,
                        unique=True,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "surname",
                    models.CharField(
                        db_comment="Client's surname",
                        max_length=255,
                        verbose_name="Surname",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_comment="Client's name",
                        max_length=255,
                        verbose_name="Название",
                    ),
                ),
                (
                    "patronymic",
                    models.CharField(
                        blank=True,
                        db_comment="Client's patronymic (if exists)",
                        max_length=255,
                        null=True,
                        verbose_name="Patronymic",
                    ),
                ),
            ],
            options={
                "verbose_name": "Client",
                "verbose_name_plural": "Clients",
                "db_table": "jw_client",
            },
        ),
        migrations.CreateModel(
            name="Social",
            fields=[
                (
                    "guid",
                    models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
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
                    "user_id",
                    models.CharField(
                        blank=True,
                        db_comment="Social id",
                        max_length=50,
                        null=True,
                        verbose_name="Telegram id",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        db_comment="Social username",
                        max_length=255,
                        null=True,
                        verbose_name="Username",
                    ),
                ),
                (
                    "client_guid",
                    models.ForeignKey(
                        db_column="client_guid",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="client_socials",
                        to="app_clients.client",
                        verbose_name="Client GUID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Social",
                "verbose_name_plural": "Socials",
                "db_table": "jw_social",
            },
        ),
        migrations.AddConstraint(
            model_name="social",
            constraint=models.UniqueConstraint(
                condition=models.Q(("user_id", None), _negated=True),
                fields=("social_type", "user_id"),
                name="uq_jw_social_user_id",
            ),
        ),
        migrations.AddConstraint(
            model_name="social",
            constraint=models.UniqueConstraint(
                condition=models.Q(("username", None), _negated=True),
                fields=("social_type", "username"),
                name="uq_jw_social_username",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="social",
            unique_together={("social_type", "client_guid")},
        ),
    ]
