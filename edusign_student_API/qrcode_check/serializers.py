import qrcode
import hashlib
from datetime import datetime, timedelta
from io import BytesIO
from django.core.files import File

from rest_framework import serializers
from .models import QRCodeGenerator, Lesson, CustomUser, Presence

# QRCode :

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

class QRCodeValidationSerializer(serializers.Serializer):
    scanned_qr = serializers.CharField()
    student = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    def validate(self, data):
        student = data.get('student')
        scanned_qr = data.get('scanned_qr')
        now = datetime.now()

        lesson = Lesson.objects.filter(promotion=student.promotion, date_debut__lte=now, date_fin__gte=now).first()

        if not lesson:
            raise serializers.ValidationError("No ongoing lesson found.")

        if student.promotion != lesson.promotion:
            raise serializers.ValidationError("You are not part of the promotion for this lesson.")

        time_slot = now.timestamp() // 10
        qr_code_generator = QRCodeGenerator.objects.get(lesson=lesson)
        expected_qr_content = hashlib.sha256(f"{lesson.id}{lesson.intervening.id}{time_slot}{qr_code_generator.secret_key}".encode()).hexdigest()

        if expected_qr_content != scanned_qr:
            raise serializers.ValidationError("Invalid QR code.")

        return data

    def save(self, **kwargs):
        student = self.validated_data.get('student')
        lesson = Lesson.objects.filter(promotion=student.promotion).first()
        presence_instance, created = Presence.objects.get_or_create(student=student, lesson=lesson)
        if not presence_instance.is_present:
            presence_instance.is_present = True
            presence_instance.save()
