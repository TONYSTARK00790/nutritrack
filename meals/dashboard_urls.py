from django.urls import path
from meals.views import dashboard_view
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
