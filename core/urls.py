from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='my_profile'), # Renamed for clarity
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('create_service/', views.create_service_view, name='create_service'),
    path('service/<int:pk>/', views.service_detail_view, name='service_detail'),
    path('service/<int:pk>/accept/', views.accept_service_view, name='accept_service'),
    path('service/<int:pk>/complete/', views.complete_service_view, name='complete_service'),
    path('service/<int:pk>/review/', views.create_review_view, name='create_review'),
]
