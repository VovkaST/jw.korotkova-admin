from django.db import models
from django.forms import model_to_dict


class SingletonModel(models.Model):
    instance = None
    entity_class = None

    class Meta:
        abstract = True

    def __new__(cls, *args, **kwargs):
        if args or kwargs:
            return super().__new__(cls)

        if not cls.instance or not cls.instance.id:
            cls.instance, created = cls.objects.get_or_create(id=1)
        else:
            cls.instance.refresh_from_db()

        return cls.instance

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def as_entity(self):
        return self.entity_class(**{k: v for k, v in model_to_dict(self).items() if v is not None})
