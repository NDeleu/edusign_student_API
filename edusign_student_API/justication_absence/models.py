from django.db import models
from django.core.validators import FileExtensionValidator
from enum import Enum

from authentication.models import CustomUser, UserStatus
from lessons.models import Presence

class ReasonList(Enum):
    SICKNESS = 'sickness'
    FAMILYDEATH = 'familydeath'
    ALARMCLOCKFAILURE = 'alarmclockfailure'
    OTHERREASON = 'otherreason'

class Justification(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="justifications", verbose_name="related_justification_student")
    absence_reason = models.CharField(max_length=20, choices=[(absence_reason.value, absence_reason.value) for absence_reason in ReasonList], default=ReasonList.OTHERREASON.value, verbose_name='justification_absence_reason')
    date_debut = models.DateField(null=False, verbose_name='start_absence_justified_date')
    date_fin = models.DateField(null=False, verbose_name='end_absence_justified_date')
    proof_document = models.FileField(upload_to="proof_documents/", verbose_name="proof_of_absence", validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    is_validate = models.BooleanField(null=True, blank=True, default=None, verbose_name="is_justification_validated")

    def __str__(self):
        if self.is_validate:
            status = "Validated"
        elif self.is_validate == False:
            status = "Not Validated"
        else:
            status = "Not already check"
        return f"Justification from {self.student.email} - {status}"
