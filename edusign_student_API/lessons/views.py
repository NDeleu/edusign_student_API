from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from lessons.serializers import (LessonCreateSerializer, LessonListSerializer, LessonDetailSerializer, 
                                 LessonUpdateSerializer, ClassRoomCreateSerializer, ClassRoomListSerializer, 
                                 ClassRoomUpdateSerializer, LessonListForUserSerializer, LessonDetailForUserSerializer,
                                 PresenceCreateSerializer, PresenceListSerializer, PresenceDetailSerializer, PresenceUpdateSerializer,
                                 Lesson, ClassRoom, Presence, CustomUser, UserStatus)
from authentication.permissions import IsAdministrator, IsAdministratorOrIntervening, IsSelforAdministratorOrIntervening

# CRUD Lesson:

class LessonCreateView(CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = (IsAuthenticated, IsAdministrator,)

class LessonListView(ListAPIView):
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)

class LessonListForUserView(ListAPIView):
    serializer_class = LessonListForUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.filter(promotion=user.promotion)

class LessonDetailView(RetrieveAPIView):
    serializer_class = LessonDetailSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)
    lookup_field = 'id'

class LessonDetailForUserView(RetrieveAPIView):
    serializer_class = LessonDetailForUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.filter(promotion=user.promotion)

class LessonUpdateView(RetrieveUpdateAPIView):
    serializer_class = LessonUpdateSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsAdministrator,)
    lookup_field = 'id'

class LessonDeleteView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsAdministrator,)
    lookup_field = 'id'

# CRUD ClassRoom:

class ClassRoomCreateView(CreateAPIView):
    serializer_class = ClassRoomCreateSerializer
    permission_classes = (IsAuthenticated, IsAdministrator,)

class ClassRoomListView(ListAPIView):
    serializer_class = ClassRoomListSerializer
    queryset = ClassRoom.objects.all()
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)

class ClassRoomUpdateView(RetrieveUpdateAPIView):
    serializer_class = ClassRoomUpdateSerializer
    queryset = ClassRoom.objects.all()
    permission_classes = (IsAuthenticated, IsAdministrator,)
    lookup_field = 'id'

class ClassRoomDeleteView(DestroyAPIView):
    queryset = ClassRoom.objects.all()
    permission_classes = (IsAuthenticated, IsAdministrator,)
    lookup_field = 'id'

# CRUD Presence :

class PresenceCreateView(CreateAPIView):
    serializer_class = PresenceCreateSerializer
    permission_classes = (IsAuthenticated, IsAdministrator,)

class PresenceListOfLessonView(ListAPIView):
    serializer_class = PresenceListSerializer
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        return Presence.objects.filter(lesson__id=lesson_id)

class PresenceDetailView(RetrieveAPIView):
    serializer_class = PresenceDetailSerializer
    queryset = Presence.objects.all()
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)
    lookup_field = 'id'

class PresenceUpdateView(RetrieveUpdateAPIView):
    serializer_class = PresenceUpdateSerializer
    queryset = Presence.objects.all()
    permission_classes = (IsAuthenticated, IsAdministratorOrIntervening,)
    lookup_field = 'id'
    
class PresenceCountForUser(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsSelforAdministratorOrIntervening,)

    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        date_now = datetime.now()

        user = CustomUser.objects.filter(id=user_id, status=UserStatus.STUDENT.value).first()
        if not user:
            raise ValidationError("L'utilisateur sélectionné n'est pas un étudiant.")

        presence_count = Presence.objects.filter(student__id=user_id, lesson__date_debut__lte=date_now).count()

        return Response({'student_lessons_count': presence_count})
    
class AbsenceCountForUser(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsSelforAdministratorOrIntervening,)

    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        date_now = datetime.now()

        user = CustomUser.objects.filter(id=user_id, status=UserStatus.STUDENT.value).first()
        if not user:
            raise ValidationError("L'utilisateur sélectionné n'est pas un étudiant.")

        absence_count = Presence.objects.filter(student__id=user_id, lesson__date_debut__lte=date_now, is_present=False).count()

        return Response({'student_absences_count': absence_count})
    
class AbsenceRateForUser(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsSelforAdministratorOrIntervening,)
    
    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        date_now = datetime.now()

        user = CustomUser.objects.filter(id=user_id, status=UserStatus.STUDENT.value).first()
        if not user:
            raise ValidationError("L'utilisateur sélectionné n'est pas un étudiant.")

        total_lessons_count = Presence.objects.filter(student__id=user_id, lesson__date_debut__lte=date_now).count()
        absences_count = Presence.objects.filter(student__id=user_id, lesson__date_debut__lte=date_now, is_present=False).count()

        if total_lessons_count == 0:
            absence_rate = 0
        else:
            absence_rate = (absences_count * 100) / total_lessons_count

        return Response({'absence_rate': absence_rate})