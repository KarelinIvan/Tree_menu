from django.db import models
from django.urls import reverse, NoReverseMatch

NULLABLE = {'blank': True, 'null': True}

class MenuItem(models.Model):
    name = models.CharField( max_length=100)
    named_url = models.CharField(
        max_length=100,
        **NULLABLE
    )
    explicit_url = models.CharField(
        max_length=200,
        **NULLABLE
    )
    menu_name = models.CharField(
        max_length=100,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        **NULLABLE
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.name

    def get_url(self):
        """ Если именованный URL не найден (NoReverseMatch), метод вернёт '#' вместо ошибки """
        if self.explicit_url:
            return self.explicit_url
        elif self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return '#'
