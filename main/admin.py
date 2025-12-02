from django.contrib import admin
from main.models import Resume, Skill, JobResult, SavedJob, APIKey


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'phone', 'resume_score', 'uploaded_at')
    search_fields = ('user__username', 'full_name', 'email')
    list_filter = ('uploaded_at', 'file_type')
    readonly_fields = ('uploaded_at', 'updated_at')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'resume')
    search_fields = ('name',)
    list_filter = ('proficiency',)


@admin.register(JobResult)
class JobResultAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'match_score', 'fetched_at')
    search_fields = ('title', 'company')
    list_filter = ('fetched_at', 'job_type')
    readonly_fields = ('fetched_at',)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    search_fields = ('user__username', 'job__title')
    list_filter = ('saved_at',)
    readonly_fields = ('saved_at',)


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('api_name', 'is_active', 'updated_at')
    list_filter = ('is_active', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
