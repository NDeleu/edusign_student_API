import uuid
from django.db import models

from lessons.models import Lesson, Presence
from authentication.models import CustomUser

class QRCodeGenerator(models.Model):
    lesson = models.OneToOneField(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='qrcode_s_lesson',
        verbose_name='related_qrcode_lesson'
    )
    secret_key = models.CharField(
        max_length=255, 
        unique=True, 
        default=str(uuid.uuid4),
        verbose_name='secret_key_string'
    )
    qr_code = models.ImageField(
        upload_to="qr_codes/", 
        null=True, 
        blank=True,
        verbose_name='qr_code_image'
    )
    expiration_time = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='expiration_time_datetime'
    )

    def __str__(self):
        return f"QRCode for {self.lesson.name}"
