from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

from accounts.forms import UserRegistrationForm, UserLoginForm
from main.models import Resume, Skill, JobResult, SavedJob, APIKey
from main.forms import ResumeUploadForm, JobSearchForm
from main.services import parse_resume_file
from main.job_api import get_recommended_jobs, search_jobs_by_keyword

import os
import tempfile
from pathlib import Path


@require_http_methods(["GET", "POST"])
def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to AI Resume Screening.')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid credentials.')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["GET"])
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')


@login_required(login_url='login')
@require_http_methods(["GET"])
def dashboard(request):
    """User dashboard"""
    try:
        resume = Resume.objects.get(user=request.user)
        resume_score = resume.resume_score
        skills_count = len(resume.skills) if resume.skills else 0
        jobs_count = JobResult.objects.filter(resume=resume).count()
        saved_jobs_count = SavedJob.objects.filter(user=request.user).count()
        
        context = {
            'resume': resume,
            'resume_score': resume_score,
            'skills_count': skills_count,
            'jobs_count': jobs_count,
            'saved_jobs_count': saved_jobs_count,
            'has_resume': True,
        }
    except Resume.DoesNotExist:
        context = {
            'resume': None,
            'resume_score': 0,
            'skills_count': 0,
            'jobs_count': 0,
            'saved_jobs_count': 0,
            'has_resume': False,
        }
    
    return render(request, 'main/dashboard.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def upload_resume(request):
    """Resume upload and parsing"""
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = request.FILES['resume']
            
            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.name).suffix) as tmp_file:
                for chunk in resume_file.chunks():
                    tmp_file.write(chunk)
                tmp_path = tmp_file.name
            
            try:
                # Parse resume
                parsed_data = parse_resume_file(tmp_path)
                
                if parsed_data:
                    # Save or update resume in database
                    resume, created = Resume.objects.get_or_create(user=request.user)
                    
                    resume.full_name = parsed_data.get('full_name', '')
                    resume.email = parsed_data.get('email', '')
                    resume.phone = parsed_data.get('phone', '')
                    resume.skills = parsed_data.get('skills', [])
                    resume.experience = parsed_data.get('experience', [])
                    resume.education = parsed_data.get('education', [])
                    resume.certifications = parsed_data.get('certifications', [])
                    resume.projects = parsed_data.get('projects', [])
                    resume.resume_score = parsed_data.get('resume_score', 0)
                    resume.keyword_insights = parsed_data.get('keyword_insights', [])
                    resume.file_type = parsed_data.get('file_type', '')
                    resume.save()
                    
                    # Clear old skills
                    Skill.objects.filter(resume=resume).delete()
                    
                    # Save skills
                    for skill in parsed_data.get('skills', []):
                        Skill.objects.create(
                            resume=resume,
                            name=skill.get('name', ''),
                            proficiency=skill.get('proficiency', 'intermediate')
                        )
                    
                    messages.success(request, 'Resume uploaded and parsed successfully!')
                    return redirect('resume_details')
                else:
                    messages.error(request, 'Failed to parse resume. Please try again.')
            
            finally:
                # Delete temporary file
                try:
                    os.unlink(tmp_path)
                except:
                    pass
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = ResumeUploadForm()
    
    return render(request, 'main/upload_resume.html', {'form': form})


@login_required(login_url='login')
@require_http_methods(["GET"])
def resume_details(request):
    """Display parsed resume details"""
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        messages.error(request, 'No resume found. Please upload one first.')
        return redirect('upload_resume')
    
    skills = Skill.objects.filter(resume=resume)
    
    context = {
        'resume': resume,
        'skills': skills,
    }
    
    return render(request, 'main/resume_details.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def clear_resume(request):
    """Clear/delete the user's resume and associated data"""
    try:
        resume = Resume.objects.get(user=request.user)
        resume_name = resume.full_name or 'Your resume'
        
        # Delete associated skills
        Skill.objects.filter(resume=resume).delete()
        
        # Delete the resume
        resume.delete()
        
        messages.success(request, f'{resume_name} has been cleared successfully. You can upload a new resume anytime.')
    except Resume.DoesNotExist:
        messages.error(request, 'No resume found to clear.')
    
    return redirect('upload_resume')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def job_recommendations(request):
    """Show job recommendations based on resume"""
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        messages.error(request, 'Please upload your resume first.')
        return redirect('upload_resume')
    
    # Get API key (uses default from job_api.py if not in database)
    from main.job_api import DEFAULT_JSEARCH_API_KEY
    try:
        api_key_obj = APIKey.objects.get(api_name='jsearch', is_active=True)
        api_key = api_key_obj.api_key
    except APIKey.DoesNotExist:
        api_key = DEFAULT_JSEARCH_API_KEY  # Use hardcoded default
    
    form = JobSearchForm(request.POST or None)
    jobs = []
    total_jobs = 0
    
    if request.method == 'POST' and form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        location = form.cleaned_data.get('location')
        job_type = form.cleaned_data.get('job_type')
        min_score = form.cleaned_data.get('min_match_score', 0)
        
        try:
            if keyword:
                # Search by keyword
                jobs = search_jobs_by_keyword(keyword, api_key, location)
            else:
                # Get recommendations based on resume skills
                jobs = get_recommended_jobs(resume.skills, api_key, location)
            
            # Filter by match score
            jobs = [job for job in jobs if job.get('match_score', 0) >= min_score]
            
            # Filter by job type
            if job_type:
                jobs = [job for job in jobs if job.get('job_type', '').upper() == job_type]
            
            total_jobs = len(jobs)
        except Exception as e:
            error_msg = str(e)
            messages.error(request, f"API Error: {error_msg}")
            jobs = []
            total_jobs = 0
    else:
        # Default: show recommendations based on resume skills
        try:
            jobs = get_recommended_jobs(resume.skills, api_key)
            total_jobs = len(jobs)
        except Exception as e:
            error_msg = str(e)
            messages.error(request, f"API Error: {error_msg}")
            jobs = []
            total_jobs = 0
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Check which jobs are saved
    saved_job_ids = SavedJob.objects.filter(
        user=request.user
    ).values_list('job_id', flat=True)
    
    context = {
        'resume': resume,
        'form': form,
        'page_obj': page_obj,
        'total_jobs': total_jobs,
        'saved_job_ids': list(saved_job_ids),
        'api_key_configured': api_key != 'PLACEHOLDER',
    }
    
    return render(request, 'main/job_recommendations.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def save_job(request, job_id):
    """Save a job"""
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Resume not found'})
    
    try:
        job = JobResult.objects.get(job_id=job_id)
    except JobResult.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Job not found'})
    
    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    
    if created:
        return JsonResponse({'success': True, 'message': 'Job saved successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Job already saved'})


@login_required(login_url='login')
@require_http_methods(["POST"])
def unsave_job(request, job_id):
    """Unsave a job"""
    try:
        saved_job = SavedJob.objects.get(user=request.user, job__job_id=job_id)
        saved_job.delete()
        return JsonResponse({'success': True, 'message': 'Job removed from saved'})
    except SavedJob.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Job not found in saved'})


@login_required(login_url='login')
@require_http_methods(["GET"])
def saved_jobs(request):
    """View saved jobs"""
    saved_jobs_list = SavedJob.objects.filter(user=request.user).select_related('job')
    
    # Pagination
    paginator = Paginator(saved_jobs_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_saved': saved_jobs_list.count(),
    }
    
    return render(request, 'main/saved_jobs.html', context)


def home(request):
    """Home page"""
    return render(request, 'home.html')
