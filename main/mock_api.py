"""
Mock Job Search API for testing when RapidAPI is unavailable
Provides sample job data for development and testing
"""

MOCK_JOBS = [
    {
        'job_id': 'mock_001',
        'title': 'Senior Python Developer',
        'company': 'Tech Innovations Inc',
        'location': 'Bangalore, India',
        'salary': 'INR 1,200,000 - 1,600,000',
        'job_type': 'FULLTIME',
        'description': 'We are looking for a Senior Python Developer with 5+ years of experience. Required skills: Python, Django, REST APIs, PostgreSQL, Docker, AWS',
        'apply_link': '#',
        'posted_date': '2025-12-01T00:00:00Z',
    },
    {
        'job_id': 'mock_002',
        'title': 'Full Stack JavaScript Developer',
        'company': 'Digital Solutions Ltd',
        'location': 'Mumbai, India',
        'salary': 'INR 900,000 - 1,300,000',
        'job_type': 'FULLTIME',
        'description': 'Looking for Full Stack JavaScript Developer. Skills: React, Node.js, MongoDB, Express, JavaScript',
        'apply_link': '#',
        'posted_date': '2025-12-01T00:00:00Z',
    },
    {
        'job_id': 'mock_003',
        'title': 'Data Scientist',
        'company': 'Analytics Pro',
        'location': 'Hyderabad, India',
        'salary': 'INR 1,000,000 - 1,500,000',
        'job_type': 'FULLTIME',
        'description': 'Seeking Data Scientist with expertise in Machine Learning. Skills: Python, SQL, ML, TensorFlow, Data Analysis',
        'apply_link': '#',
        'posted_date': '2025-12-01T00:00:00Z',
    },
    {
        'job_id': 'mock_004',
        'title': 'DevOps Engineer',
        'company': 'Cloud Systems',
        'location': 'Pune, India',
        'salary': 'INR 1,100,000 - 1,400,000',
        'job_type': 'FULLTIME',
        'description': 'DevOps Engineer needed for infrastructure management. Skills: Docker, Kubernetes, AWS, CI/CD, Linux',
        'apply_link': '#',
        'posted_date': '2025-12-01T00:00:00Z',
    },
    {
        'job_id': 'mock_005',
        'title': 'Frontend React Developer',
        'company': 'Web Design Studios',
        'location': 'Delhi, India',
        'salary': 'INR 700,000 - 1,100,000',
        'job_type': 'FULLTIME',
        'description': 'Experienced React Developer wanted. Skills: React, JavaScript, CSS, HTML, Redux, Material-UI',
        'apply_link': '#',
        'posted_date': '2025-12-01T00:00:00Z',
    },
]

def get_mock_jobs(query=None, location=None, num_jobs=10):
    """Return mock jobs for testing"""
    return MOCK_JOBS[:num_jobs]
