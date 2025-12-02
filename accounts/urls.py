from django.urls import path
from accounts import views
from main import views as main_views

urlpatterns = [
    path('register/', main_views.register, name='register'),
    path('login/', main_views.login_view, name='login'),
    path('logout/', main_views.logout_view, name='logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/resumes/', views.admin_resumes, name='admin_resumes'),
    path('admin/api-keys/', views.admin_api_keys, name='admin_api_keys'),
]
