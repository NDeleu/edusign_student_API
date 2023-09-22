from rest_framework import serializers

from .models import Justification, CustomUser, UserStatus, Presence

# CRUD Justification :

class JustificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justification
        fields = ["absence_reason", "date_debut", "date_fin", "proof_document"]

    def validate(self, data):
        user = self.context['request'].user
        if not user.status == UserStatus.STUDENT.value:
            raise serializers.ValidationError("Only students can create a justification.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        justification = Justification.objects.create(student=user, **validated_data)
        if 'proof_document' in validated_data:
            justification.proof_document.save(f"{justification.id}.pdf", validated_data['proof_document'])
            justification.save()
        return justification

class JustificationListForStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justification
        fields = ["id", "date_debut", "date_fin", "is_validate"]

class JustificationListForAdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justification
        fields = ["id", "student", "date_debut", "date_fin", "is_validate"]

class JustificationDetailForStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justification
        fields = ["id", "absence_reason", "date_debut", "date_fin", "proof_document", "is_validate"]

class JustificationDetailForAdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justification
        fields = ["id", "student", "absence_reason", "date_debut", "date_fin", "proof_document", "is_validate"]

class JustificationUpdateForStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justification
        fields = ["absence_reason", "date_debut", "date_fin", "proof_document"]

    def validate(self, data):
        if self.instance.is_validate is not None:
            raise serializers.ValidationError("Justification has already been reviewed.")
        return data
    
    def update(self, instance, validated_data):
        # handle the usual fields
        for attr, value in validated_data.items():
            if attr != 'proof_document':
                setattr(instance, attr, value)
                
        if 'proof_document' in validated_data:
            instance.proof_document.save(f"{instance.id}.pdf", validated_data['proof_document'])
            
        instance.save()
        return instance

class JustificationUpdateForAdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justification
        fields = ["is_validate"]
