from django.urls import path

from . import views

app_name = 'lesson'

urlpatterns = [
    # CRUD Lesson:
    path('create/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('list/', views.LessonListView.as_view(), name='lesson_list'),
    path('user-list/', views.LessonListForUserView.as_view(), name='lesson_user_list'),
    path('detail/<int:id>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('user-detail/<int:id>/', views.LessonDetailForUserView.as_view(), name='lesson_user_detail'),
    path('update/<int:id>/', views.LessonUpdateView.as_view(), name='lesson_update'),
    path('delete/<int:id>/', views.LessonDeleteView.as_view(), name='lesson_delete'),

    # CRUD ClassRoom:
    path('classroom/create/', views.ClassRoomCreateView.as_view(), name='classroom_create'),
    path('classroom/list/', views.ClassRoomListView.as_view(), name='classroom_list'),
    path('classroom/update/<int:id>/', views.ClassRoomUpdateView.as_view(), name='classroom_update'),
    path('classroom/delete/<int:id>/', views.ClassRoomDeleteView.as_view(), name='classroom_delete'),
    
    # CRUD Presence:
    path('presence/create/', views.PresenceCreateView.as_view(), name='presence_create'),
    path('presence/list-by-lesson/<int:lesson_id>/', views.PresenceListOfLessonView.as_view(), name='presence_list_by_lesson'),
    path('presence/detail/<int:id>/', views.PresenceDetailView.as_view(), name='presence_detail'),
    path('presence/update/<int:id>/', views.PresenceUpdateView.as_view(), name='presence_update'),
    
    # Count Presence and Absence :
    path('presence/my-lessons-count/', views.PresenceCountForSelf.as_view(), name='presence_my_lessons_count'),
    path('presence/my-absences-count/', views.AbsenceCountForSelf.as_view(), name='presence_my_absences_count'),
    path('presence/my-absence-rate/', views.AbsenceRateForSelf.as_view(), name='presence_my_absence_rate'),
    path('presence/user-lessons-count/<int:user_id>/', views.PresenceCountForUser.as_view(), name='presence_user_lessons_count'),
    path('presence/user-absences-count/<int:user_id>/', views.AbsenceCountForUser.as_view(), name='presence_user_absences_count'),
    path('presence/user-absence-rate/<int:user_id>/', views.AbsenceRateForUser.as_view(), name='presence_user_absence_rate'),
]
