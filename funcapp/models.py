from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Funktion(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="funcs",
                               verbose_name='пользователь')
    func = models.CharField(max_length=200, verbose_name='функция')
    interval = models.PositiveIntegerField(default=5,
                                           verbose_name='интервал t, дней')
    step = models.PositiveIntegerField(default=1, verbose_name='шаг t, часы')
    last_date = models.DateTimeField(auto_now_add=True,
                                     verbose_name='дата обработки')
    plot = models.ImageField(upload_to='funcapp/', blank=True, null=True,
                             verbose_name='график')
    errorfield = models.CharField(max_length=200, blank=True, null=True,
                                  verbose_name='ошибка')

    def save(self):
        super().save()
        return self.pk

    class Meta:
        verbose_name = 'функцию'
        verbose_name_plural = "функции"
