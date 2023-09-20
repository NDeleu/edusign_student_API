from rest_framework.permissions import BasePermission
from .models import CustomUser

class IsAdministrator(BasePermission):
    """
    Autorise l'accès uniquement aux utilisateurs ayant le statut d'administrateur.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.status == CustomUser.ADMINISTRATOR)
    
class IsIntervening(BasePermission):
    """
    Autorise l'accès uniquement aux utilisateurs ayant le statut d'intervenant.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.status == CustomUser.INTERVENING)
