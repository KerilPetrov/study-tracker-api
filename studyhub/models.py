from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Plan(models.Model):
    """Модель планов обучения"""
    title = models.CharField(
        verbose_name='Название',
        max_length=100,
        blank=False,
        null=False,
        unique=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        max_length=1024,
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        related_name='plans',
        null=False,
    )
    created_at = models.DateTimeField(
        verbose_name="Время и дата создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Время и дата изменения",
        auto_now_add=True,
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'План обучения'
        verbose_name_plural = 'Планы обучения'

    def __str__(self):
        return f"{self.title} ({self.owner})"


class Topic(models.Model):
    """Модель тем обучения"""
    plan = models.ForeignKey(
        Plan,
        verbose_name='План обучения',
        on_delete=models.CASCADE,
        related_name='topics',
        null=False,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=100,
        blank=False,
        null=False
    )
    description = models.TextField(
        verbose_name="Описание",
        max_length=1024,
        blank=True,
        null=True
    )
    order = models.IntegerField(
        verbose_name='Порядковый номер',
        default=0
    )
    estimated_days = models.PositiveIntegerField(
        verbose_name='Расчетное количество дней',
        null=True,
        blank=True,
    )
    is_optional = models.BooleanField(
        verbose_name='Обязательность',
        default=False,
    )

    class Meta:
        ordering = ['order']
        unique_together = ['plan', 'order']
        verbose_name = 'Тема обучения'
        verbose_name_plural = 'Темы обучения'

    def __str__(self):
        return self.title


class Task(models.Model):
    """Модель тем обучения"""
    topic = models.ForeignKey(
        Topic,
        verbose_name='Задача',
        on_delete=models.CASCADE,
        related_name='tasks',
        null=False,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=100,
        blank=False,
        null=False
    )
    is_done = models.BooleanField(
        verbose_name='Выполняемость',
        default=False,
    )
    estimated_minutes = models.PositiveIntegerField(
        verbose_name='Расчетное время (в минутах)',
        null=True,
        blank=True,
    )
    actual_minutes = models.PositiveIntegerField(
        verbose_name='Фактическое время (в минутах)',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Время и дата создания",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Задача темы обучения'
        verbose_name_plural = 'Задачи тем обучения'

    def __str__(self):
        return self.title
