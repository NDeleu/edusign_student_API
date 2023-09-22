from rest_framework import serializers
from datetime import timedelta

from .models import CustomUser, Lesson, UserStatus, ClassRoom, Presence
from authentication.serializers import PromotionDetailSerializer, UserDetailSerializer

# CRUD Lesson :

class LessonCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lesson
        fields = ['name', 'date_debut', 'date_fin', 'description', 'intervening', 'classroom', 'promotion']

    def validate_intervening(self, value):
        if value.status != UserStatus.INTERVENING.value:
            raise serializers.ValidationError("L'utilisateur sélectionné n'est pas un intervenant.")
        return value

    def validate_date_debut(self, value):
            value -= timedelta(hours=2)
            return value 
    
    def validate_date_fin(self, value):
        value -= timedelta(hours=2)
        return value

    def validate(self, data):
        date_debut = data['date_debut']
        date_fin = data['date_fin']

        for field in ['intervening', 'classroom', 'promotion']:
            conflicting_lessons = Lesson.objects.filter(
                **{
                    field: data[field],
                    "date_debut__lt": date_fin,
                    "date_fin__gt": date_debut
                }
            )
            
            if conflicting_lessons.exists():
                raise serializers.ValidationError(f"Le {field} sélectionné a déjà un cours pendant ce créneau.")

        return data

    def save(self, **kwargs):
        lesson = super().save(**kwargs)

        students = CustomUser.objects.filter(promotion=lesson.promotion, status=UserStatus.STUDENT.value)
        for student in students:
            Presence.objects.create(student=student, lesson=lesson)

        return lesson

class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'date_debut', 'date_fin', 'intervening', 'classroom', 'promotion']
        
class LessonListForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'date_debut', 'date_fin', 'classroom']

class LessonDetailSerializer(serializers.ModelSerializer):
    promotion_details = PromotionDetailSerializer(source='promotion', read_only=True)

    class Meta:
        model = Lesson
        fields = ['name', 'date_debut', 'date_fin', 'description', 'intervening', 'classroom', 'promotion', 'promotion_details']

class LessonDetailForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'date_debut', 'date_fin', 'description', 'intervening', 'classroom']

class LessonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'date_debut', 'date_fin', 'description', 'intervening', 'classroom']

    def validate_intervening(self, value):
        if value.status != UserStatus.INTERVENING.value:
            raise serializers.ValidationError("L'utilisateur sélectionné n'est pas un intervenant.")
        return value
    
    def validate_date_debut(self, value):
            value -= timedelta(hours=2)
            return value 
    
    def validate_date_fin(self, value):
        value -= timedelta(hours=2)
        return value

    def validate(self, data):
        date_debut = data.get('date_debut', self.instance.date_debut)
        date_fin = data.get('date_fin', self.instance.date_fin)

        for field in ['intervening', 'classroom', 'promotion']:
            field_value = data.get(field, getattr(self.instance, field))
            
            conflicting_lessons = Lesson.objects.filter(
                **{
                    field: field_value,
                    "date_debut__lt": date_fin,
                    "date_fin__gt": date_debut
                }
            ).exclude(id=self.instance.id)
            
            if conflicting_lessons.exists():
                raise serializers.ValidationError(f"Le {field} sélectionné a déjà un cours pendant ce créneau.")

        return data

# CRUD ClassRoom :

class ClassRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['name']

class ClassRoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'name']

class ClassRoomUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['name']
        
# CRUD Presence :

class PresenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = ['student', 'lesson']
        
    def validate_student(self, value):
        if value.status != UserStatus.STUDENT.value:
            raise serializers.ValidationError("L'utilisateur sélectionné n'est pas un étudiant.")
        return value

    def validate(self, data):
        student = data.get('student')
        lesson = data.get('lesson')

        if student.promotion != lesson.promotion:
            raise serializers.ValidationError("L'étudiant n'appartient pas à la promotion associée à cette leçon.")

        return data

class PresenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = ['id', 'is_present', 'student', 'lesson']
        
class PresenceDetailSerializer(serializers.ModelSerializer):
    lesson_details = LessonDetailForUserSerializer(read_only=True)
    student_details = UserDetailSerializer(read_only=True)

    class Meta:
        model = Presence
        fields = ['id', 'is_present', 'student', 'student_details', 'lesson', 'lesson_details']

        
class PresenceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = ['is_present']
        