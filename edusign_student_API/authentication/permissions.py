from rest_framework.permissions import BasePermission
from .models import UserStatus

class IsAdministrator(BasePermission):
    """
    Allow access only to users with the status of administrator.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.status == UserStatus.ADMINISTRATOR.value)
    
class IsIntervening(BasePermission):
    """
    Allow access only to users with the status of intervening.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.status == UserStatus.INTERVENING.value)
    
class IsStudent(BasePermission):
    """
    Allow access only to users with the status of student.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.status == UserStatus.STUDENT.value)

class IsAdministratorOrIntervening(BasePermission):
    """
    Allow access only to users with the status of administrator or intervening.
    """
    def has_permission(self, request, view):
        return bool(request.user and (request.user.status == UserStatus.ADMINISTRATOR.value or request.user.status == UserStatus.INTERVENING.value))
    
class IsSelforAdministrator(BasePermission):
    """
    Allow access only to users with the status of administrator, or themselves.
    """
    def has_permission(self, request, view):
        is_self = str(request.user.id) == view.kwargs.get('user_id', "")
        return bool(request.user and (request.user.status == UserStatus.ADMINISTRATOR.value or is_self))
    
class IsSelforAdministratorOrIntervening(BasePermission):
    """
    Allow access only to users with the status of administrator, intervening, or themselves.
    """
    def has_permission(self, request, view):
        is_self = str(request.user.id) == view.kwargs.get('user_id', "")
        return bool(request.user and (request.user.status in [UserStatus.ADMINISTRATOR.value, UserStatus.INTERVENING.value] or is_self))

