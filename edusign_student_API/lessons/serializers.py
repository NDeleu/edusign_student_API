from rest_framework import serializers

from .models import Lesson, UserStatus, ClassRoom
from authentication.serializers import PromotionDetailSerializer

# CRUD Lesson :

class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'date_debut', 'date_fin', 'description', 'intervening', 'classroom', 'promotion']

    def validate_intervening(self, value):
        """
        Vérifie que l'intervenant choisi a le statut 'intervening'
        """
        if value.status != UserStatus.INTERVENING.value:
            raise serializers.ValidationError("L'utilisateur sélectionné n'est pas un intervenant.")
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

class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'date_debut', 'date_fin', 'intervening', 'classroom', 'promotion']

class LessonDetailSerializer(serializers.ModelSerializer):
    promotion_details = PromotionDetailSerializer(source='promotion', read_only=True)

    class Meta:
        model = Lesson
        fields = ['name', 'date_debut', 'date_fin', 'description', 'intervening', 'classroom', 'promotion', 'promotion_details']

class LessonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'date_debut', 'date_fin', 'description', 'intervening', 'classroom', 'promotion']

    def validate_intervening(self, value):
        """
        Vérifie que l'intervenant choisi a le statut 'intervening'
        """
        if value.status != UserStatus.INTERVENING.value:
            raise serializers.ValidationError("L'utilisateur sélectionné n'est pas un intervenant.")
        return value

    def validate(self, data):
        date_debut = data.get('date_debut', self.instance.date_debut)
        date_fin = data.get('date_fin', self.instance.date_fin)

        for field in ['intervening', 'classroom', 'promotion']:
            # Obtenez la valeur du champ de data ou de l'instance actuelle si elle n'est pas fournie dans data
            field_value = data.get(field, getattr(self.instance, field))
            
            # Trouvez les leçons qui sont déjà en conflit pour ce champ, excluant la leçon actuellement mise à jour
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