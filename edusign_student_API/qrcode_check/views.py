from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from django.utils import timezone


from .serializers import QRCodeGeneratorUpdateSerializer, QRCodeGeneratorDetailSerializer, Lesson, QRCodeGenerator, QRCodeValidationSerializer
from authentication.permissions import IsIntervening, IsStudent

# QRCode :

class QRCodeGeneratorView(APIView):
    permission_classes = (IsAuthenticated, IsIntervening,)

    def get(self, request):
        now = timezone.now()

        lesson = Lesson.objects.filter(intervening=request.user, date_debut__lte=now, date_fin__gte=now).first()
        if not lesson:
            return Response({"error": "No ongoing lesson found."}, status=400)

        qr_code_generator, created = QRCodeGenerator.objects.get_or_create(lesson=lesson)

        if not qr_code_generator.qr_code or qr_code_generator.expiration_time <= now:
            serializer = QRCodeGeneratorUpdateSerializer(qr_code_generator, data={})
            if serializer.is_valid(raise_exception=True):
                qr_code_generator = serializer.save()

        detail_serializer = QRCodeGeneratorDetailSerializer(qr_code_generator)
        return Response(detail_serializer.data)

class ValidateQRCode(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        serializer = QRCodeValidationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": "Presence marked successfully."}, status=HTTP_200_OK)

