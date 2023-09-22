import qrcode
import hashlib
from datetime import datetime, timedelta
from io import BytesIO
from django.core.files import File

from rest_framework import serializers
from .models import QRCodeGenerator, Lesson

class QRCodeGeneratorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCodeGenerator
        fields = ['qr_code', 'expiration_time']

    def update(self, instance, validated_data):
        now = datetime.now()
        time_slot = now.timestamp() // 10
        lesson = instance.lesson
        hashed_data = hashlib.sha256(f"{lesson.id}{lesson.intervening.id}{time_slot}{instance.secret_key}".encode()).hexdigest()
        
        qr_image = qrcode.make(hashed_data)
        qr_image_io = BytesIO()
        qr_image.save(qr_image_io, format='PNG')
        filename = f"qr_{lesson.id}.png"
        
        instance.qr_code.save(filename, File(qr_image_io), save=False)
        instance.expiration_time = now + timedelta(seconds=10)
        instance.save()
        return instance

class QRCodeGeneratorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCodeGenerator
        fields = ['qr_code', 'expiration_time']
