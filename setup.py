#!/usr/bin/env python
"""
AI Resume Screening System - Setup Script
Run this to quickly set up the application
"""

import os
import sys
import django
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_resume_screening.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import APIKey

def create_superuser():
    """Create a superuser account"""
    print("\n" + "="*60)
    print("CREATE SUPERUSER ACCOUNT")
    print("="*60)
    
    if User.objects.filter(username='admin').exists():
        print("✓ Admin user already exists!")
        return
    
    print("\nEnter admin credentials:")
    username = input("Username (default: admin): ").strip() or "admin"
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    if not email or not password:
        print("✗ Email and password are required!")
        return
    
    try:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"\n✓ Superuser '{username}' created successfully!")
    except Exception as e:
        print(f"✗ Error creating superuser: {e}")

def setup_api_keys():
    """Setup JSearch API key"""
    print("\n" + "="*60)
    print("API KEY CONFIGURATION")
    print("="*60)
    
    api_key_obj = APIKey.objects.filter(api_name='jsearch').first()
    
    if api_key_obj:
        print(f"\n✓ JSearch API Key already configured!")
        print(f"  Status: {'Active' if api_key_obj.is_active else 'Inactive'}")
        change = input("Do you want to update it? (y/n): ").lower()
        if change != 'y':
            return
    
    print("\nGet your JSearch API key from:")
    print("1. Visit: https://rapidapi.com/letscrape-6bfc-api-6301/api/jsearch")
    print("2. Sign up and subscribe to the free plan")
    print("3. Copy your API key\n")
    
    api_key = input("Enter your JSearch API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("✗ Skipping API key setup")
        return
    
    try:
        APIKey.objects.update_or_create(
            api_name='jsearch',
            defaults={'api_key': api_key, 'is_active': True}
        )
        print("\n✓ JSearch API key configured successfully!")
    except Exception as e:
        print(f"✗ Error saving API key: {e}")

def print_next_steps():
    """Print next steps"""
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Start the server: python manage.py runserver")
    print("2. Visit: http://localhost:8000/")
    print("3. Admin panel: http://localhost:8000/admin/")
    print("\nFeatures:")
    print("✓ Register and login")
    print("✓ Upload and parse resume (PDF/DOCX)")
    print("✓ View extracted information")
    print("✓ Get job recommendations")
    print("✓ Save favorite jobs")
    print("✓ Admin dashboard with analytics")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════╗
║   AI RESUME SCREENING & JOB RECOMMENDATION SYSTEM          ║
║                    Setup Wizard                            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    create_superuser()
    setup_api_keys()
    print_next_steps()
