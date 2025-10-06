from django.urls import path
from . import views

urlpatterns = [
    path('team/', views.team_view, name='team_view'),
    path('leaders/', views.leaders_view, name='leaders_view'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]