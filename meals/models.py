from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название продукта')
    calories = models.PositiveIntegerField(
        verbose_name='Калорийность на 100г (ккал)'
    )
    proteins = models.FloatField(
        verbose_name='Белки на 100г (г)'
    )
    fats = models.FloatField(
        verbose_name='Жиры на 100г (г)'
    )
    carbs = models.FloatField(
        verbose_name='Углеводы на 100г (г)'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']
    def __str__(self):
        return f'{self.name} ({self.calories} ккал/100г)'
        