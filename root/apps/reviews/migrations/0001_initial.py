import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "screenshot",
                    models.ImageField(
                        db_comment="Messenger screenshot",
                        upload_to="reviews/screenshots/%Y/%m/",
                        verbose_name="Screenshot",
                    ),
                ),
                (
                    "client_label",
                    models.CharField(
                        blank=True,
                        db_comment="Short caption, e.g. name or age",
                        max_length=200,
                        verbose_name="Client label",
                    ),
                ),
                (
                    "quote",
                    models.TextField(
                        blank=True,
                        db_comment="Optional text excerpt",
                        verbose_name="Quote",
                    ),
                ),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        db_comment="Optional 1–5 stars",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                        verbose_name="Rating",
                    ),
                ),
                (
                    "sort_order",
                    models.PositiveIntegerField(
                        db_comment="Lower first on the site",
                        default=0,
                        verbose_name="Sort order",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        db_comment="Show on landing",
                        default=True,
                        verbose_name="Published",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
            ],
            options={
                "verbose_name": "Review",
                "verbose_name_plural": "Reviews",
                "db_table": "jw_review",
                "ordering": ("sort_order", "-created_at"),
            },
        ),
    ]
