# AI Resume Screening & Job Recommendation System

A comprehensive Django application for intelligent resume parsing, analysis, and AI-driven job recommendations.

## Features

### User Management
- **User Registration & Authentication**: Secure account creation and login
- **Email-based Login**: Sign in using email and password
- **User Dashboard**: Personalized dashboard showing resume statistics and quick actions

### Resume Parsing
- **Supported Formats**: PDF and DOCX files (max 5MB)
- **Automatic Information Extraction**:
  - Full name and contact information
  - Skills detection with proficiency levels
  - Work experience and companies
  - Education and certifications
  - Projects and achievements
  - Keyword insights
- **Resume Scoring**: Overall profile quality score (0-100%)
- **Secure Processing**: Temporary file handling with automatic deletion after parsing

### Job Recommendations
- **AI-Powered Matching**: Jobs matched based on extracted skills and experience
- **JSearch API Integration**: Free API for job search (requires RapidAPI key)
- **Smart Filtering**:
  - Filter by keyword, location, and job type
  - Minimum match score threshold
  - Pagination for easy navigation
- **Job Saving**: Bookmark jobs for later review
- **Match Score Calculation**: See how well each job matches your resume

### Admin Dashboard
- **System Statistics**: Total users, resumes, and skill analytics
- **Top Skills Chart**: View most common skills among users
- **User Management**: View and manage all registered users
- **Resume Management**: Browse all uploaded and parsed resumes
- **API Key Configuration**: Configure JSearch API keys from the dashboard

### UI/UX
- **Modern Bootstrap 5 Design**: Responsive and mobile-friendly interface
- **Smooth Animations**: Fade-in effects and transitions
- **Interactive Elements**: Cards, badges, icons, and visual feedback
- **Intuitive Navigation**: Clear navigation and user flows
- **Collapsible Sidebar**: Space-saving navigation (can be extended)
- **Dark-themed Navbar**: Professional appearance

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Windows/Linux/Mac

### Step 1: Clone/Setup Project
```bash
cd your_project_directory
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install django python-docx spacy nltk requests pillow
python -m spacy download en_core_web_sm
```

### Step 4: Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### Step 6: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit: `http://localhost:8000/`

## Configuration

### Step 1: Add JSearch API Key

1. **Get API Key**:
   - Visit [RapidAPI JSearch](https://rapidapi.com/letscrape-6bfc-api-6301/api/jsearch)
   - Sign up or log in to RapidAPI
   - Subscribe to the free plan
   - Copy your API key

2. **Add to System**:
   - Go to Admin Dashboard (`/accounts/admin/dashboard/`)
   - Click "Configure API Keys"
   - Select "JSearch API (RapidAPI)"
   - Paste your API key
   - Click "Save API Key"

### Step 2: Test the System

1. **Register a new account**: `/accounts/register/`
2. **Upload a resume**: Dashboard → Upload Resume
3. **View parsed data**: Dashboard → Resume Details
4. **Get job recommendations**: Dashboard → Find Jobs
5. **Save jobs**: Click the Save button on any job

## Project Structure

```
ai_resume_screening/
├── ai_resume_screening/          # Project configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # URL routing
│   └── wsgi.py                  # WSGI configuration
├── accounts/                     # Authentication app
│   ├── views.py                 # Admin views
│   ├── urls.py                  # Account URLs
│   ├── forms.py                 # Registration/Login forms
│   └── migrations/              # Database migrations
├── main/                         # Core app
│   ├── models.py                # Database models
│   ├── views.py                 # Main views
│   ├── urls.py                  # App URLs
│   ├── forms.py                 # App forms
│   ├── services.py              # Resume parsing logic
│   ├── job_api.py               # Job API integration
│   ├── admin.py                 # Admin configuration
│   └── migrations/              # Database migrations
├── templates/                    # HTML templates
│   ├── base.html                # Base template
│   ├── home.html                # Home page
│   ├── accounts/                # Auth templates
│   ├── main/                    # App templates
│   └── admin/                   # Admin templates
├── static/                       # Static files
│   ├── css/                     # Stylesheets
│   └── js/                      # JavaScript files
├── manage.py                     # Django management
└── db.sqlite3                    # SQLite database
```

## Models

### Resume
- User (OneToOne)
- Parsed information (name, email, phone)
- Skills, experience, education, certifications, projects
- Resume score and keyword insights

### Skill
- Resume (ForeignKey)
- Skill name and proficiency level

### JobResult
- Resume (ForeignKey)
- Job details (title, company, location, salary)
- Match score and matching skills

### SavedJob
- User (ForeignKey)
- Job (ForeignKey)
- Notes for the job

### APIKey
- API name and key storage
- Active/inactive status

## Database Schema

```
User (Django Auth)
    │
    ├─→ Resume (1:1)
    │    ├─→ Skill (1:M)
    │    └─→ JobResult (1:M)
    │
    └─→ SavedJob (1:M)
         └─→ JobResult

APIKey (Global)
```

## API Integration

### JSearch API

**Endpoint**: `https://jsearch.p.rapidapi.com/search`

**Features**:
- Job search with multiple parameters
- India-focused results
- Salary range extraction
- Company and location data

**Placeholder Integration**:
- The system uses placeholder keys during development
- Replace with your actual API key in Admin Dashboard
- Graceful handling when API key is not configured

## Resume Parsing

### Extraction Process

1. **File Upload**: PDF/DOCX validation and temporary storage
2. **Text Extraction**: Uses Python-DOCX for DOCX, PyPDF2 for PDF
3. **NLP Processing**: spaCy for NER (Named Entity Recognition)
4. **Information Extraction**:
   - **Name**: From NER PERSON entities
   - **Email**: Regex pattern matching
   - **Phone**: Regex pattern for phone numbers
   - **Skills**: Database matching with proficiency estimation
   - **Experience**: Company extraction from ORG entities
   - **Education**: Keyword matching for degrees
5. **Scoring**: Based on data completeness
6. **Storage**: Data stored in database, file deleted
7. **Cleanup**: Temporary files securely removed

### Supported Skills

**Programming**: Python, Java, JavaScript, TypeScript, C++, C#, PHP, Ruby, Go, Rust, Kotlin

**Web**: React, Angular, Vue, HTML, CSS, Express, Django, Flask, Spring, ASP.NET

**Database**: SQL, MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch

**Cloud**: AWS, Azure, GCP, Docker, Kubernetes, Terraform

**Data**: Pandas, NumPy, TensorFlow, PyTorch, Scikit-learn, Matplotlib, Tableau

**DevOps**: Jenkins, GitLab, GitHub, CI/CD, Linux

## Customization

### Add More Skills

Edit `main/services.py` - `ResumeParser.COMMON_SKILLS`:

```python
'category': ['skill1', 'skill2', 'skill3'],
```

### Modify Resume Scoring

Edit `main/services.py` - `calculate_resume_score()` method to adjust weights.

### Change API Providers

Edit `main/job_api.py` to integrate different job search APIs.

### Customize UI

Edit `templates/base.html` and individual templates to modify styling.

## Security Features

- CSRF protection on forms
- Password validation and hashing
- Email uniqueness validation
- Secure file upload with type checking
- API key configuration in admin only
- Login required decorators
- Staff-only admin access

## Performance Tips

- Use pagination for large job lists (10 items per page)
- Cache API responses if needed
- Database indexes on frequently searched fields
- Compress static files for production

## Troubleshooting

### No spaCy model found
```bash
python -m spacy download en_core_web_sm
```

### NLTK stopwords not found
```python
import nltk
nltk.download('stopwords')
```

### API key not working
- Verify key in Admin Dashboard
- Check RapidAPI account status
- Ensure API subscription is active

### Resume parsing fails
- Check file format (PDF/DOCX only)
- Verify file size < 5MB
- Ensure sufficient disk space

### Jobs not showing
- Confirm API key is configured
- Check network connectivity
- Verify RapidAPI subscription

## Future Enhancements

- [ ] Email notifications for new jobs
- [ ] Resume templates and builders
- [ ] LinkedIn profile integration
- [ ] Advanced analytics and charts
- [ ] Job application tracking
- [ ] Multiple resume support per user
- [ ] Skill proficiency assessment tests
- [ ] Interview preparation resources
- [ ] Salary prediction based on skills
- [ ] Company insights and reviews

## Deployment

### For Production:

1. **Set `DEBUG = False`** in settings.py
2. **Use PostgreSQL** instead of SQLite
3. **Configure allowed hosts** in settings.py
4. **Use environment variables** for sensitive data
5. **Enable HTTPS** with SSL certificate
6. **Use Gunicorn** as WSGI server
7. **Configure Nginx** as reverse proxy
8. **Set up static file serving** with WhiteNoise or CDN
9. **Use scheduled tasks** (Celery) for heavy processing
10. **Enable database backups**

## Support & Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [spaCy Documentation](https://spacy.io/usage)
- [NLTK Documentation](https://www.nltk.org/)
- [RapidAPI JSearch](https://rapidapi.com/letscrape-6bfc-api-6301/api/jsearch)

## License

This project is open source and available for educational and commercial use.

## Author

Created with ❤️ for intelligent job matching and resume screening.

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Status**: Production Ready
#   a i _ r e s u m e _ s c r e e n i n g  
 