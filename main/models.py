from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date


class Coach(models.Model):
    name = models.CharField('Имя тренера', max_length=30)
    age = models.IntegerField('Возраст', null=True, blank=True)
    qualification = models.CharField('Специализация', max_length=30, null=True, blank=True)
    experience = models.CharField('Опыт работы', max_length=30, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='static/assets/css/img')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'



class GymMembership(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название абонемента')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    duration_months = models.IntegerField(verbose_name='Продолжительность (месяцев)')
    visit_amount = models.IntegerField('Количество посещений в неделю', default=0)
    app_access = models.CharField('Доступ к приложению с онлайн-тренировками', max_length=10, default="Нет")
    features = models.TextField(blank=True, null=True, verbose_name='Особенности абонемента')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Членство'
        verbose_name_plural = 'Членства в фитнес-центре'

class SubPlan(models.Model):
    months = models.CharField('Количество месяцев', max_length=30)
    coefficient = models.IntegerField('Коэффициент')

    def str(self):
        return f'{self.months} месяцев, Коэффициент: {self.coefficient}'

    class Meta:
        verbose_name = 'План членства'
        verbose_name_plural = 'Планы членств'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='coachs/')
    selected_membership = models.ForeignKey(GymMembership, on_delete=models.SET_NULL, null=True, blank=True)
    selected_plan = models.ForeignKey(SubPlan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Workouts(models.Model):
    name = models.CharField('Название тренировки', max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'

class Schedule(models.Model):
    day_of_week = models.CharField(max_length=10, default='День')
    start_time = models.TimeField(default='23:59:59')
    end_time = models.TimeField(default='23:59:59')
    trainer_name = models.ForeignKey(Coach, on_delete=models.SET_NULL, blank=True, null=True)
    training_name = models.ForeignKey(Workouts, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f"{self.trainer_name} - {self.day_of_week} - {self.start_time}-{self.end_time} - {self.training_name}"

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



