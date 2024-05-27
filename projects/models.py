from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=100, default="Название проекта", unique=True)
    sorted_index = models.IntegerField(default=1, null=True)
    description = models.CharField(max_length=2000, default="Описание проекта")
    url = models.CharField(max_length=100, default="После развертки появится")
    model = models.FileField(blank=True, default='model')
    image = models.ImageField(default=None)
    MODEL_STATUS = [
        (0, "Нет модели"),
        (1, "Поднятие job"),
        (2, "Модель загружается"),
        (3, "Модель развернута"),
        (4, "Модель не прошла валидацию")
    ]
    status = models.IntegerField(verbose_name='Статус модели', choices=MODEL_STATUS, default=0)
    catalog = models.CharField(max_length=100, default="Категория каталога 1")
    user_id = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    users_list = models.ManyToManyField(related_name="project_list", to=User)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
