from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('training-style/', views.training_style_view, name='training_style'),
    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),
    path('api/chat/create/', views.create_chat_session, name='create_chat_session'),
    path('api/chat/send/', views.send_chat_message, name='send_chat_message'),
]
