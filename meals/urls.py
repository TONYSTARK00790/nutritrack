from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('', views.meal_list, name='meal_list'),
    path('unified/', views.nutrition_unified, name='nutrition_unified'),
    path('add/', views.add_meal, name='add_meal'),
    path('<int:pk>/edit/', views.edit_meal, name='edit_meal'),
    path('<int:pk>/adjust/', views.adjust_quantity, name='adjust_quantity'),
    path('<int:pk>/delete/', views.delete_meal, name='delete_meal'),
    path('foods/', views.food_database, name='food_database'),
    path('foods/add/', views.add_food, name='add_food'),
    path('foods/<int:pk>/api/', views.food_detail_api, name='food_detail_api'),
]
