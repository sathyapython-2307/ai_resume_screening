from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.db.models import Count

from accounts.forms import UserRegistrationForm, UserLoginForm
from main.models import Resume, APIKey

# Admin views
@login_required(login_url='login')
@require_http_methods(["GET"])
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    total_users = User.objects.count()
    total_resumes = Resume.objects.count()
    
    # Get skill statistics
    all_skills = []
    for resume in Resume.objects.all():
        if resume.skills:
            all_skills.extend(resume.skills)
    
    skill_count = {}
    for skill in all_skills:
        skill_name = skill.get('name', 'Unknown')
        skill_count[skill_name] = skill_count.get(skill_name, 0) + 1
    
    top_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    context = {
        'total_users': total_users,
        'total_resumes': total_resumes,
        'top_skills': top_skills,
    }
    
    return render(request, 'admin/dashboard.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def admin_users(request):
    """Admin: View all users"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    users = User.objects.annotate(resume_count=Count('resume'))
    
    context = {
        'users': users,
    }
    
    return render(request, 'admin/users.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def admin_resumes(request):
    """Admin: View all resumes"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    resumes = Resume.objects.all().select_related('user')
    
    context = {
        'resumes': resumes,
    }
    
    return render(request, 'admin/resumes.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def admin_api_keys(request):
    """Admin: Manage API keys"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        api_name = request.POST.get('api_name')
        api_key = request.POST.get('api_key')
        
        if api_name and api_key:
            obj, created = APIKey.objects.update_or_create(
                api_name=api_name,
                defaults={'api_key': api_key, 'is_active': True}
            )
            messages.success(request, f'API key updated for {api_name}')
            return redirect('admin_api_keys')
    
    api_keys = APIKey.objects.all()
    
    context = {
        'api_keys': api_keys,
    }
    
    return render(request, 'admin/api_keys.html', context)
