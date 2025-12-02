from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('resume-details/', views.resume_details, name='resume_details'),
    path('resume-details/clear/', views.clear_resume, name='clear_resume'),
    path('job-recommendations/', views.job_recommendations, name='job_recommendations'),
    path('saved-jobs/', views.saved_jobs, name='saved_jobs'),
    path('save-job/<str:job_id>/', views.save_job, name='save_job'),
    path('unsave-job/<str:job_id>/', views.unsave_job, name='unsave_job'),
]
