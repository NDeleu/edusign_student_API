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
    intervening = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        verbose_name='related_lesson_intervening',
        related_name='lesson_s_intervening'
    )
    classroom = models.ForeignKey(
        ClassRoom, 
        on_delete=models.CASCADE, 
        verbose_name='related_lesson_classroom',
        related_name='lesson_s_classroom'
    )
    promotion = models.ForeignKey(
        Promotion, 
        on_delete=models.CASCADE, 
        verbose_name='related_lesson_promotion',
        related_name='lesson_s_promotion'
    )

    def __str__(self):
        return self.name

class Presence(models.Model):
    is_present = models.BooleanField(default=False, verbose_name='is_present_bool')
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='related_student',
        related_name='presence_s_student'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='related_lesson',
        related_name='presence_s_lesson'
    )
    
    class Meta:
        unique_together = ('student', 'lesson')
        