from django import forms
from django.contrib.auth.models import User
from main.models import Resume, SavedJob


class ResumeUploadForm(forms.Form):
    """Form for resume upload"""
    resume = forms.FileField(
        label='Upload Resume',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.docx',
            'id': 'resumeFile'
        }),
        help_text='Supported formats: PDF, DOCX (Max 5MB)'
    )
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        
        if resume:
            # Check file extension
            valid_extensions = ['.pdf', '.docx']
            file_name = resume.name.lower()
            
            if not any(file_name.endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError("Only PDF and DOCX files are allowed.")
            
            # Check file size (5MB limit)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size should not exceed 5MB.")
        
        return resume


class JobSearchForm(forms.Form):
    """Form for job search filters"""
    keyword = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by keyword, skill, or job title'
        })
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location (optional)'
        })
    )
    job_type = forms.ChoiceField(
        choices=[
            ('', 'All Types'),
            ('FULLTIME', 'Full Time'),
            ('PARTTIME', 'Part Time'),
            ('CONTRACTOR', 'Contract'),
            ('TEMPORARY', 'Temporary'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    min_match_score = forms.IntegerField(
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum match score',
            'min': '0',
            'max': '100'
        })
    )


class SaveJobForm(forms.ModelForm):
    """Form to save jobs"""
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add notes about this job (optional)'
        }),
        required=False
    )
    
    class Meta:
        model = SavedJob
        fields = ['notes']
