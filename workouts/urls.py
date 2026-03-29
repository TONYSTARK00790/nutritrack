from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.workout_list, name='list'),
    path('browse/', views.all_workouts, name='browse'),
    path('log/<int:pk>/', views.log_workout, name='log'),
    path('history/', views.workout_history, name='history'),
    path('<int:pk>/', views.workout_detail, name='detail'),
    path('start/<int:pk>/', views.start_workout, name='start'),
    path('sessions/', views.sessions_list, name='sessions'),
    path('sessions/complete/<int:pk>/', views.mark_complete, name='mark_complete'),
    
    # Custom routine routes
    path('routines/create/', views.create_custom_routine, name='create_routine'),
    path('routines/my/', views.my_routines, name='my_routines'),
    path('routines/<int:pk>/', views.routine_detail, name='routine_detail'),
    path('routines/<int:pk>/edit/', views.edit_routine, name='edit_routine'),
    path('routines/<int:pk>/delete/', views.delete_routine, name='delete_routine'),
    path('routines/<int:pk>/add-workout/', views.add_workout_to_routine, name='add_workout'),
    path('routines/<int:pk>/remove-workout/<int:workout_pk>/', views.remove_workout_from_routine, name='remove_workout'),
]
