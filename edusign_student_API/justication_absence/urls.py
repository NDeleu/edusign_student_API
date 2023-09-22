from django.urls import path

from . import views

app_name = 'justification'

urlpatterns = [
    # CRUD Justification :
    path('create/', views.JustificationCreateView.as_view(), name='justification-create'),
    path('list/student/', views.JustificationListForStudentView.as_view(), name='justification-list-student'),
    path('list/administrator/', views.JustificationListForAdministratorView.as_view(), name='justification-list-administrator'),
    path('list/administrator/<int:user_id>/', views.JustificationListForAdministratorView.as_view(), name='justification-list-administrator-user'),
    path('detail/student/<int:id>/', views.JustificationDetailForStudentView.as_view(), name='justification-detail-student'),
    path('detail/administrator/<int:id>/', views.JustificationDetailForAdministratorView.as_view(), name='justification-detail-administrator'),
    path('update/student/<int:id>/', views.JustificationUpdateForStudentView.as_view(), name='justification-update-student'),
    path('update/administrator/<int:id>/', views.JustificationUpdateForAdministratorView.as_view(), name='justification-update-administrator'),
    path('delete/<int:id>/', views.JustificationDeleteView.as_view(), name='justification-delete'),
    
    # Count Justified :
    path('unjustified/self/', views.UnjustifiedAbsenceForSelf.as_view(), name='unjustified-absence-self'),
    path('unjustified/<int:user_id>/', views.UnjustifiedAbsenceForUser.as_view(), name='unjustified-absence-user'),
]
