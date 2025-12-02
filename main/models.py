from django.db import models
from django.contrib.auth.models import User
import json


class Resume(models.Model):
    """Model to store resume information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    file_path = models.CharField(max_length=500, null=True, blank=True)
    
    # Extracted Information
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    
    # JSON fields for complex data
    skills = models.JSONField(default=list, blank=True)
    experience = models.JSONField(default=list, blank=True)
    education = models.JSONField(default=list, blank=True)
    certifications = models.JSONField(default=list, blank=True)
    projects = models.JSONField(default=list, blank=True)
    
    # Resume scoring
    resume_score = models.FloatField(default=0.0)
    keyword_insights = models.JSONField(default=list, blank=True)
    
    # Metadata
    file_type = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('docx', 'DOCX')], null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Resume - {self.user.username}"


class Skill(models.Model):
    """Model to store individual skills extracted from resume"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skill_objects')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ], default='intermediate')
    
    class Meta:
        unique_together = ('resume', 'name')
    
    def __str__(self):
        return f"{self.name} - {self.proficiency}"


class JobResult(models.Model):
    """Model to store job search results"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='job_results')
    
    job_id = models.CharField(max_length=500, unique=True)
    title = models.CharField(max_length=300)
    company = models.CharField(max_length=300)
    location = models.CharField(max_length=300, null=True, blank=True)
    salary = models.CharField(max_length=200, null=True, blank=True)
    job_type = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    apply_link = models.URLField(max_length=500)
    
    # Match score based on resume skills
    match_score = models.FloatField(default=0.0)
    matching_skills = models.JSONField(default=list, blank=True)
    
    # Metadata
    fetched_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=100, default='jsearch')
    
    def __str__(self):
        return f"{self.title} - {self.company}"


class SavedJob(models.Model):
    """Model to store saved jobs by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(JobResult, on_delete=models.CASCADE, related_name='saved_by_users')
    
    saved_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'job')
    
    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"


class APIKey(models.Model):
    """Model to store API configurations"""
    API_CHOICES = [
        ('jsearch', 'JSearch API (RapidAPI)'),
    ]
    
    api_name = models.CharField(max_length=100, choices=API_CHOICES, unique=True)
    api_key = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.api_name} API Key"
