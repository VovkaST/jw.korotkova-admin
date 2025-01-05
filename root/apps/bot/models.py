from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from root.apps.bot.managers import ButtonsQuerySet
from root.base.models import CreatedTimestampModel, TimedModel


class Bot(TimedModel):
    name = models.CharField(_("Unique name"), max_length=100, unique=True, db_comment="Bot unique name")
    version = models.CharField(_("Version"), max_length=20, db_comment="Bot`s version")
    description = models.CharField(_("Description"), max_length=1000, db_comment="Bot`s description")
    welcome_message = models.CharField(_("Welcome message"), max_length=1000, db_comment="Welcome message")

    class Meta:
        db_table = "bot_info"
        verbose_name = _("Bot")
        verbose_name_plural = _("Bots")

    def __str__(self):
        return f"{self.name} (v.{self.version})"


class UserChat(CreatedTimestampModel):
    username = models.CharField(_("Username"), max_length=255, null=True, blank=True, db_comment="User's name")
    user_id = models.CharField(
        _("User ID"), max_length=100, unique=True, db_comment="User ID", validators=[validators.MinLengthValidator(1)]
    )
    chat_id = models.CharField(
        _("Chat ID"), max_length=100, unique=True, db_comment="Chat ID", validators=[validators.MinLengthValidator(1)]
    )

    class Meta:
        db_table = "bot_user_chat"
        db_table_comment = "User's chat info"
        verbose_name = _("User chat info")
        verbose_name_plural = _("User chats infos")

    def __str__(self):
        return f"{self.user_id}:{self.chat_id})"


class Buttons(TimedModel):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, verbose_name=_("Bot"), related_name="buttons")
    text = models.CharField(_("Text"), db_index=True, db_comment="Button`s text")
    simple_response = models.CharField(
        _("Simple click response"), null=True, blank=True, db_comment="Simple click response"
    )
    sort_order = models.IntegerField(
        _("Sort order"), default=1, validators=[validators.MinValueValidator(1)], db_comment="Sort order index"
    )

    objects = ButtonsQuerySet.as_manager()

    class Meta:
        db_table = "bot_buttons"
        verbose_name = _("Button")
        verbose_name_plural = _("Buttons")
        unique_together = ["bot", "sort_order"]

    def __str__(self):
        return self.text


class Channel(models.Model):
    chat_id = models.BigIntegerField(
        _("Chat ID"),
        unique=True,
        help_text=_("Global chat identity. Usually negative integer."),
        db_comment="Chat ID",
    )
    title = models.CharField(
        _("Title"),
        max_length=255,
        help_text=_(
            "Channel name. Changing value has no effect for real channel. This is useful only for information."
        ),
        db_comment="Channel title",
    )
    link = models.CharField(
        _("Link"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Link for channel. Useful for make http-link like https://t.me/channel_name."),
        db_comment="Channel link",
    )

    class Meta:
        db_table = "bot_channel"
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")

    def __str__(self):
        return self.title
