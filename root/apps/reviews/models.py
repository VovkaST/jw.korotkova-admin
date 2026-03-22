from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    """Публичный отзыв со скриншотом переписки (управление в админке)."""

    screenshot = models.ImageField(
        _("Скриншот переписки"),
        upload_to="reviews/screenshots/%Y/%m/",
        db_comment="Скриншот из мессенджера",
    )
    client_label = models.CharField(
        _("Подпись / имя для сайта"),
        max_length=200,
        blank=True,
        db_comment="Краткая подпись к отзыву (имя, возраст и т.п.)",
    )
    quote = models.TextField(
        _("Текстовая выдержка"),
        blank=True,
        db_comment="Необязательная цитата или краткое описание",
    )
    rating = models.PositiveSmallIntegerField(
        _("Оценка"),
        null=True,
        blank=True,
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)],
        db_comment="Необязательная оценка от 1 до 5",
    )
    sort_order = models.PositiveIntegerField(
        _("Порядок сортировки"),
        default=0,
        db_comment="Меньшее значение — выше на странице",
    )
    is_published = models.BooleanField(
        _("Опубликован"),
        default=True,
        db_comment="Показывать отзыв на лендинге",
    )
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        db_table = "jw_review"
        ordering = ("sort_order", "-created_at")
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    def __str__(self) -> str:
        if self.client_label:
            return f"{_('Отзыв')}: {self.client_label}"
        return f"{_('Отзыв')} #{self.pk}"
