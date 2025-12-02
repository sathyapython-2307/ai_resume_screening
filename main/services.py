"""
Resume Parsing Service
Extracts information from PDF and DOCX files using NLP
"""
import os
import re
import string
from pathlib import Path
from docx import Document
import spacy
from nltk.corpus import stopwords
import nltk
import PyPDF2

# Download NLTK data if not already present
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


class ResumeParser:
    """Extract information from resume files"""
    
    # Common skills database
    COMMON_SKILLS = {
        'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'kotlin'],
        'web': ['react', 'angular', 'vue', 'html', 'css', 'express', 'django', 'flask', 'spring', 'asp.net'],
        'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'oracle'],
        'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
        'data': ['pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'matplotlib', 'tableau'],
        'devops': ['jenkins', 'gitlab', 'github', 'ci/cd', 'devops', 'linux'],
        'soft': ['communication', 'leadership', 'teamwork', 'problem-solving', 'critical thinking'],
    }
    
    # Email pattern
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Phone pattern (basic)
    PHONE_PATTERN = r'(?:\+?\d{1,3}[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def parse_resume(self, file_path):
        """Main method to parse resume"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.docx':
            text = self.extract_text_from_docx(file_path)
            file_type = 'docx'
        elif file_ext == '.pdf':
            text = self.extract_text_from_pdf(file_path)
            file_type = 'pdf'
        else:
            return None
        
        if not text:
            return None
        
        # Process with spaCy
        doc = nlp(text.lower())
        
        parsed_data = {
            'full_name': self.extract_name(text, doc),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'skills': self.extract_skills(text),
            'experience': self.extract_experience(text, doc),
            'education': self.extract_education(text, doc),
            'certifications': self.extract_certifications(text, doc),
            'projects': self.extract_projects(text, doc),
            'file_type': file_type,
            'raw_text': text[:1000],  # Store first 1000 chars for reference
        }
        
        # Calculate resume score
        parsed_data['resume_score'] = self.calculate_resume_score(parsed_data)
        parsed_data['keyword_insights'] = self.extract_keyword_insights(text)
        
        return parsed_data
    
    def extract_name(self, text, doc):
        """Extract full name from resume"""
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.title()
        
        # Fallback: First line might be name
        first_line = text.split('\n')[0].strip()
        if len(first_line) < 100:
            return first_line.title()
        
        return "Not Found"
    
    def extract_email(self, text):
        """Extract email address"""
        matches = re.findall(self.EMAIL_PATTERN, text)
        return matches[0] if matches else "Not Found"
    
    def extract_phone(self, text):
        """Extract phone number"""
        matches = re.findall(self.PHONE_PATTERN, text)
        if matches:
            return f"+{matches[0][0]}-{matches[0][1]}-{matches[0][2]}"
        return "Not Found"
    
    def extract_skills(self, text):
        """Extract skills from resume"""
        text_lower = text.lower()
        found_skills = []
        
        for category, skills in self.COMMON_SKILLS.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append({
                        'name': skill.upper(),
                        'category': category,
                        'proficiency': self.estimate_proficiency(text_lower, skill)
                    })
        
        return list({skill['name']: skill for skill in found_skills}.values())
    
    def estimate_proficiency(self, text, skill):
        """Estimate skill proficiency level"""
        skill_lower = skill.lower()
        count = text.count(skill_lower)
        
        if count >= 5:
            return 'Advanced'
        elif count >= 3:
            return 'Intermediate'
        else:
            return 'Beginner'
    
    def extract_experience(self, text, doc):
        """Extract work experience"""
        experience = []
        
        # Look for common experience keywords
        exp_keywords = ['experience', 'worked', 'employment', 'professional']
        text_lower = text.lower()
        
        sections = re.split(r'(experience|employment|worked)', text_lower, flags=re.IGNORECASE)
        
        if len(sections) > 1:
            exp_section = sections[-1][:1000]  # Take relevant section
            
            # Extract companies (usually proper nouns)
            companies = set()
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    companies.add(ent.text)
            
            for company in list(companies)[:5]:
                experience.append({
                    'company': company,
                    'designation': 'Professional Role',
                    'duration': 'Not extracted'
                })
        
        return experience if experience else [{'company': 'Not Found', 'designation': '', 'duration': ''}]
    
    def extract_education(self, text, doc):
        """Extract education details"""
        education = []
        
        # Look for education keywords
        edu_keywords = ['degree', 'bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'bsc', 'msc', 'university', 'college']
        text_lower = text.lower()
        
        for keyword in edu_keywords:
            if keyword in text_lower:
                edu_section = re.findall(rf'{keyword}[^.]*\.', text_lower)
                for section in edu_section[:3]:
                    education.append({
                        'degree': keyword.upper(),
                        'field': 'Computer Science',
                        'institution': 'Not extracted',
                        'year': 'Not extracted'
                    })
                break
        
        return education if education else [{'degree': 'Not Found', 'field': '', 'institution': '', 'year': ''}]
    
    def extract_certifications(self, text, doc):
        """Extract certifications"""
        certifications = []
        
        cert_keywords = ['certification', 'certified', 'aws', 'azure', 'gcp', 'cisco', 'comptia', 'pmp', 'prince2']
        text_lower = text.lower()
        
        for keyword in cert_keywords:
            if keyword in text_lower:
                certifications.append({
                    'name': keyword.upper(),
                    'issuer': 'Not extracted',
                    'year': 'Not extracted'
                })
        
        return certifications if certifications else []
    
    def extract_projects(self, text, doc):
        """Extract projects"""
        projects = []
        
        # Look for project keywords
        proj_keywords = ['project', 'built', 'developed', 'created', 'implemented']
        text_lower = text.lower()
        
        for keyword in proj_keywords:
            if keyword in text_lower:
                proj_section = re.findall(rf'{keyword}[^.]*\.', text_lower)
                for section in proj_section[:3]:
                    projects.append({
                        'name': section.strip()[:100],
                        'description': section.strip(),
                        'technologies': []
                    })
                break
        
        return projects if projects else []
    
    def calculate_resume_score(self, data):
        """Calculate overall resume score (0-100)"""
        score = 0
        
        # Name (10 points)
        if data['full_name'] != 'Not Found':
            score += 10
        
        # Email (10 points)
        if data['email'] != 'Not Found':
            score += 10
        
        # Phone (10 points)
        if data['phone'] != 'Not Found':
            score += 10
        
        # Skills (20 points)
        score += min(20, len(data['skills']) * 2)
        
        # Experience (20 points)
        if data['experience'] and data['experience'][0].get('company') != 'Not Found':
            score += 20
        
        # Education (15 points)
        if data['education'] and data['education'][0].get('degree') != 'Not Found':
            score += 15
        
        # Certifications (10 points)
        score += min(10, len(data['certifications']) * 3)
        
        # Projects (5 points)
        score += min(5, len(data['projects']))
        
        return min(100, score)
    
    def extract_keyword_insights(self, text):
        """Extract important keywords from resume"""
        text_lower = text.lower()
        
        # Remove stopwords and punctuation
        words = text_lower.split()
        keywords = [
            word.strip(string.punctuation) 
            for word in words 
            if word.strip(string.punctuation) not in self.stop_words 
            and len(word.strip(string.punctuation)) > 4
        ]
        
        # Count keyword frequency
        keyword_freq = {}
        for keyword in keywords:
            keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
        
        # Top 10 keywords
        top_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return [{'keyword': kw, 'frequency': freq} for kw, freq in top_keywords]


def parse_resume_file(file_path):
    """Helper function to parse resume"""
    parser = ResumeParser()
    return parser.parse_resume(file_path)
