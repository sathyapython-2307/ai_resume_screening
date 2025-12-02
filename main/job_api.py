"""
Job Search API Integration Service
Fetches job recommendations based on resume skills
"""
import requests
from django.core.cache import cache
import logging
import time
from main.mock_api import get_mock_jobs

logger = logging.getLogger(__name__)

# Default API Key - can be overridden in database
DEFAULT_JSEARCH_API_KEY = "ak_0kd18786e2nzusm60nw0adtx8q5rtxbrjmph67vvf5zttv2"


class JobSearchAPI:
    """Handle JSearch API requests"""
    
    BASE_URL = "https://jsearch.p.rapidapi.com/search"
    
    def __init__(self, api_key=None):
        # Use provided key or fall back to default
        self.api_key = api_key or DEFAULT_JSEARCH_API_KEY
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
    
    def search_jobs(self, query, num_pages=1, location=None):
        """
        Search for jobs using JSearch API
        
        Args:
            query: Job search query (skills/keywords)
            num_pages: Number of pages to fetch
            location: Optional location filter
        
        Returns:
            List of job results
        """
        try:
            all_jobs = []
            
            for page in range(1, num_pages + 1):
                # Check cache first
                cache_key = f"jobs_{query}_{page}_{location}"
                cached_jobs = cache.get(cache_key)
                if cached_jobs is not None:
                    all_jobs.extend(cached_jobs)
                    continue
                
                params = {
                    "query": query,
                    "page": str(page),
                    "num_pages": "1",
                    "date_posted": "month",
                    "country": "IN"  # Focus on India
                }
                
                if location:
                    params["location"] = location
                
                # Rate limiting: wait 1 second between requests
                if page > 1:
                    time.sleep(1)
                
                response = requests.get(
                    self.BASE_URL,
                    headers=self.headers,
                    params=params,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('data', [])
                    
                    page_jobs = []
                    for job in jobs:
                        page_jobs.append({
                            'job_id': job.get('job_id', ''),
                            'title': job.get('job_title', 'N/A'),
                            'company': job.get('employer_name', 'N/A'),
                            'location': job.get('job_location', 'N/A'),
                            'salary': self._extract_salary(job),
                            'job_type': job.get('job_employment_type', 'N/A'),
                            'description': job.get('job_description', ''),
                            'apply_link': job.get('job_apply_link', ''),
                            'posted_date': job.get('job_posted_at_datetime_utc', ''),
                        })
                    
                    all_jobs.extend(page_jobs)
                    # Cache results for 24 hours (86400 seconds)
                    cache.set(cache_key, page_jobs, 86400)
                elif response.status_code == 403:
                    error_msg = response.json().get('message', 'Not subscribed to API')
                    logger.error(f"API Error 403: {error_msg} - Using mock data for testing")
                    # Fall back to mock data for testing
                    logger.warning("RapidAPI subscription not active - using mock job data")
                    return get_mock_jobs(query, location, num_jobs=10)
                elif response.status_code == 429:
                    logger.error(f"API Error 429: Too many requests - Using mock data")
                    # Fall back to mock data when rate limited
                    return get_mock_jobs(query, location, num_jobs=5)
                else:
                    error_msg = response.json().get('message', response.text) if response.headers.get('content-type') == 'application/json' else response.text
                    logger.error(f"API Error: {response.status_code} - {error_msg}")
                    raise Exception(f"API Error {response.status_code}: {error_msg}")
                    
            return all_jobs
            
        except Exception as e:
            logger.error(f"Error in search_jobs: {str(e)}")
            raise
    
    def _extract_salary(self, job_data):
        """Extract salary information"""
        min_salary = job_data.get('job_min_salary')
        max_salary = job_data.get('job_max_salary')
        currency = job_data.get('job_salary_currency', 'INR')
        
        if min_salary and max_salary:
            return f"{currency} {min_salary:,} - {max_salary:,}"
        elif min_salary:
            return f"{currency} {min_salary:,}"
        elif max_salary:
            return f"{currency} {max_salary:,}"
        
        return "Salary not disclosed"


class JobRecommendationEngine:
    """Engine to match resume skills with job requirements"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.api = JobSearchAPI(api_key) if api_key else None
    
    def recommend_jobs(self, resume_skills, location=None, pages=3):
        """
        Recommend jobs based on resume skills
        
        Args:
            resume_skills: List of skill objects
            location: Optional location
            pages: Number of pages to fetch
        
        Returns:
            List of recommended jobs
        """
        if not self.api:
            logger.warning("API not configured")
            return []
        
        # Build search query from top skills
        skill_names = [skill.get('name', '').lower() for skill in resume_skills[:5]]
        query = " OR ".join(skill_names) if skill_names else "developer"
        
        # Search for jobs
        jobs = self.api.search_jobs(query, num_pages=pages, location=location)
        
        # Calculate match scores
        matched_jobs = []
        for job in jobs:
            match_score, matching_skills = self._calculate_match_score(
                job,
                resume_skills
            )
            
            job['match_score'] = match_score
            job['matching_skills'] = matching_skills
            
            if match_score > 0:  # Only include jobs with at least some match
                matched_jobs.append(job)
        
        # Sort by match score
        matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matched_jobs
    
    def _calculate_match_score(self, job, resume_skills):
        """
        Calculate match score between job and resume
        
        Returns:
            Tuple of (score, matching_skills)
        """
        job_description = (
            job.get('description', '') + ' ' + 
            job.get('title', '') + ' ' +
            job.get('company', '')
        ).lower()
        
        matching_skills = []
        score = 0
        
        for skill in resume_skills:
            skill_name = skill.get('name', '').lower()
            if skill_name in job_description:
                matching_skills.append(skill_name)
                score += 10
        
        # Bonus for exact title matches
        job_title_lower = job.get('title', '').lower()
        for skill in resume_skills:
            skill_name = skill.get('name', '').lower()
            if skill_name in job_title_lower:
                score += 5
        
        # Normalize score to 0-100
        score = min(100, score)
        
        return score, matching_skills


def get_recommended_jobs(resume_skills, api_key=None, location=None, pages=2):
    """
    Helper function to get job recommendations
    Uses provided api_key or falls back to DEFAULT_JSEARCH_API_KEY
    """
    # Use provided key or fall back to default
    api_key_to_use = api_key or DEFAULT_JSEARCH_API_KEY
    
    if not api_key_to_use or api_key_to_use.strip() == 'PLACEHOLDER':
        logger.warning("API key not configured")
        return []
    
    engine = JobRecommendationEngine(api_key=api_key_to_use)
    return engine.recommend_jobs(resume_skills, location=location, pages=pages)


def search_jobs_by_keyword(keyword, api_key, location=None):
    """
    Helper function to search jobs by keyword
    """
    if not api_key or api_key.strip() == 'PLACEHOLDER':
        logger.warning("API key not configured")
        return []
    
    api = JobSearchAPI(api_key=api_key)
    return api.search_jobs(keyword, num_pages=2, location=location)
