from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class ClassRoom(models.Model):

    name = models.CharField(max_length=128, verbose_name='classroomname')

class Promo(models.Model):

    name = models.CharField(max_length=128, verbose_name='promoname')
    # One to many (user many => promo one)

class Lesson(models.Model):

    name = models.CharField(max_length=128, verbose_name='lessonname')
    # date time start
    # date time end
    # descriptions
    # foreign key Classroom one to one et empêcher plusieurs ClassRoom suivant horaires
    # foreign key User mais status intervenant uniquement
    # foreign key ? ref promo : necessaire pour find all User relatifs

class Justificatif(models.Model):
    # gestion images / pdf
    # relation absence ?
    pass

class Absence(models.Model):
    # foreign user
    # foreign lessons
    # foreign justif ?
    pass

