from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.db.models import Q
from rest_framework import filters

from .serializers import (JustificationCreateSerializer, JustificationListForStudentSerializer,
                          JustificationListForAdministratorSerializer, JustificationDetailForStudentSerializer,
                          JustificationDetailForAdministratorSerializer, JustificationUpdateForStudentSerializer,
                          JustificationUpdateForAdministratorSerializer, 
                          Justification, Presence, CustomUser, UserStatus)
from authentication.permissions import IsStudent, IsAdministrator, IsAdministratorOrIntervening, IsSelforAdministrator

# CRUD Justification :

class JustificationCreateView(CreateAPIView):
    serializer_class = JustificationCreateSerializer
    permission_classes = (IsAuthenticated, IsStudent,)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            response.data = {
                "details": "Justification created successfully",
                "justification": response.data
            }
        return response

class JustificationListForStudentView(ListAPIView):
    serializer_class = JustificationListForStudentSerializer
    permission_classes = (IsAuthenticated, IsStudent,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_debut', 'date_fin']

    def get_queryset(self):
        return Justification.objects.filter(student=self.request.user)

class JustificationListForAdministratorView(ListAPIView):
    serializer_class = JustificationListForAdministratorSerializer
    permission_classes = (IsAuthenticated, IsAdministrator,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_debut', 'date_fin']

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            student = CustomUser.objects.filter(id=user_id, status=UserStatus.STUDENT.value).first()
            if not student:
                raise ValidationError("L'utilisateur sélectionné n'est pas un étudiant.")
            return Justification.objects.filter(student=student)
        return Justification.objects.all()

class JustificationDetailForStudentView(RetrieveAPIView):
    serializer_class = JustificationDetailForStudentSerializer
    permission_classes = (IsAuthenticated, IsStudent,)
    queryset = Justification.objects.all()
    lookup_field = 'id'
    
    def get_object(self):
        obj = super().get_object()
        if obj.student != self.request.user:
            raise ValidationError("Vous ne pouvez pas voir cette justification.")
        return obj

class JustificationDetailForAdministratorView(RetrieveAPIView):
    serializer_class = JustificationDetailForAdministratorSerializer
    queryset = Justification.objects.all()
    permission_classes = (IsAuthenticated, IsAdministrator,)
    lookup_field = 'id'
    
    def get_object(self):
        obj = super().get_object()
        if obj.student.status != UserStatus.STUDENT.value:
            raise ValidationError("Cette justification ne concerne pas un étudiant.")
        return obj

class JustificationUpdateForStudentView(RetrieveUpdateAPIView):
    serializer_class = JustificationUpdateForStudentSerializer
    permission_classes = (IsAuthenticated, IsStudent,)
    queryset = Justification.objects.all()
    lookup_field = 'id'

    def get_object(self):
        obj = super().get_object()
        if obj.student != self.request.user:
            raise ValidationError("Vous ne pouvez pas mettre à jour cette justification.")
        return obj

    def update(self, request, *args, **kwargs):
        justification = self.get_object()
        if justification.is_validate is not None:
            return Response({"error": "Justification has already been reviewed."}, status=HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

class JustificationUpdateForAdministratorView(RetrieveUpdateAPIView):
    serializer_class = JustificationUpdateForAdministratorSerializer
    queryset = Justification.objects.all()
    permission_classes = (IsAuthenticated, IsAdministrator,)
    lookup_field = 'id'
    
    def get_object(self):
        obj = super().get_object()
        if obj.student.status != UserStatus.STUDENT.value:
            raise ValidationError("Cette justification ne concerne pas un étudiant.")
        return obj
    
class JustificationDeleteView(DestroyAPIView):
    queryset = Justification.objects.all()
    permission_classes = (IsAuthenticated, IsSelforAdministrator,)
    lookup_field = 'id'

    def get_object(self):
        obj = super().get_object()
        if obj.student.status != UserStatus.STUDENT.value:
            raise ValidationError("La justification concernée ne vient pas d'un étudiant.")
        return obj

# Count Justified :

class UnjustifiedAbsenceFunctions:
    def get_unjustified_absences_count(absences, justifications):
        absences = sorted(absences, key=lambda x: x.lesson.date_debut)
        justifications = sorted(justifications, key=lambda x: x.date_debut)
        
        absence_pointer, justification_pointer = 0, 0
        unjustified_count = 0

        while absence_pointer < len(absences) and justification_pointer < len(justifications):
            absence = absences[absence_pointer]
            justification = justifications[justification_pointer]
            
            if absence.lesson.date_debut <= justification.date_fin and absence.lesson.date_fin >= justification.date_debut:
                # Absence is justified by this justification, move to next absence
                absence_pointer += 1
            elif absence.lesson.date_fin < justification.date_debut:
                # Absence is not justified and predates the current justification, mark as unjustified and move to next absence
                unjustified_count += 1
                absence_pointer += 1
            else:
                # Move to the next justification as the current justification doesn't justify this absence
                justification_pointer += 1

        # Count any remaining absences as unjustified
        unjustified_count += len(absences) - absence_pointer

        return unjustified_count

class UnjustifiedAbsenceForSelf(RetrieveAPIView, UnjustifiedAbsenceFunctions):
    permission_classes = (IsAuthenticated, IsStudent,)

    def retrieve(self, request, *args, **kwargs):
        absences = Presence.objects.filter(student=request.user, is_present=False)
        justifications = Justification.objects.filter(student=request.user, is_validate=True)

        unjustified_count = self.get_unjustified_absences_count(absences, justifications)

        return Response({'unjustified_absence_count': unjustified_count})

class UnjustifiedAbsenceForUser(RetrieveAPIView, UnjustifiedAbsenceFunctions):
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)

    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = CustomUser.objects.filter(id=user_id, status=UserStatus.STUDENT.value).first()

        if not user:
            raise ValidationError("L'utilisateur sélectionné n'est pas un étudiant.")

        absences = Presence.objects.filter(student=user, is_present=False)
        justifications = Justification.objects.filter(student=user, is_validate=True)

        unjustified_count = self.get_unjustified_absences_count(absences, justifications)

        return Response({'unjustified_absence_count': unjustified_count})
