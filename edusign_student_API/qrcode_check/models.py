import uuid
from django.db import models

from lessons.models import Lesson

class QRCodeGenerator(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='qrcode_s_lesson')
    secret_key = models.CharField(max_length=255, unique=True, default=str(uuid.uuid4))
    qr_code = models.ImageField(upload_to="qr_codes/", null=True, blank=True)
    expiration_time = models.DateTimeField(null=True, blank=True)
