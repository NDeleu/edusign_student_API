from django.db import models

from authentication.models import CustomUser, Promotion, UserStatus

class ClassRoom(models.Model):
    name = models.CharField(max_length=128, verbose_name='classroom_name')

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=200, null=False, verbose_name='lesson_name')
    date_debut = models.DateField(null=False, verbose_name='start_date')
    date_fin = models.DateField(null=False, verbose_name='end_date')
    description = models.CharField(max_length=500, default="Without descriptions", verbose_name='description')
    intervening = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        verbose_name='related_intervening',
        related_name='lesson_s_intervening'
    )
    classroom = models.OneToOneField(
        ClassRoom, 
        on_delete=models.CASCADE, 
        verbose_name='related_classroom',
        related_name='lesson_s_classroom'
    )
    promotion = models.OneToOneField(
        Promotion, 
        on_delete=models.CASCADE, 
        verbose_name='related_promotion',
        related_name='lesson_s_promotion'
    )

    def __str__(self):
        return self.name

class Justificatif(models.Model):
    # gestion images / pdf
    # relation absence ?
    pass

class Absence(models.Model):
    # foreign user
    # foreign lessons
    # foreign justif ?
    pass

