import json
import logging
from typing import List, Dict, Any

class JobDatabase:
    """
    Job database that manages job listings data.
    In a production system, this would connect to a real database.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._jobs = self._load_sample_jobs()
    
    def _load_sample_jobs(self) -> List[Dict[str, Any]]:
        """Load sample job data for demonstration"""
        sample_jobs = [
            {
                "job_id": "RED-456",
                "title": "Senior UX Designer",
                "company": "Reddit",
                "location": "Remote in USA",
                "salary_range": [146000, 232000],
                "employment_type": "Full-Time",
                "company_size": "51-200 Employees",
                "industry": "AI & Machine Learning",
                "required_skills": ["Figma", "Prototyping", "UX Research"],
                "values_promoted": ["Impactful Work", "Transparency & Communication"],
                "experience_required": "5-8 years",
                "role_level": "Senior"
            },
            {
                "job_id": "GGL-320",
                "title": "Design Manager",
                "company": "Google",
                "location": "Mountain View, CA",
                "salary_range": [180000, 280000],
                "employment_type": "Full-Time",
                "company_size": "10000+ Employees",
                "industry": "Technology",
                "required_skills": ["Design Leadership", "Figma", "User Research"],
                "values_promoted": ["Innovation", "Mentorship & Career Development"],
                "experience_required": "7-10 years",
                "role_level": "Manager"
            },
            {
                "job_id": "AIRBNB-123",
                "title": "Product Designer",
                "company": "Airbnb",
                "location": "San Francisco, CA",
                "salary_range": [160000, 220000],
                "employment_type": "Full-Time",
                "company_size": "1000-5000 Employees",
                "industry": "Travel & Hospitality",
                "required_skills": ["Figma", "UI/UX Design", "Prototyping"],
                "values_promoted": ["Work-Life Balance", "Impactful Work"],
                "experience_required": "4-6 years",
                "role_level": "Senior"
            },
            {
                "job_id": "UBER-789",
                "title": "Senior Product Designer",
                "company": "Uber",
                "location": "Remote in USA",
                "salary_range": [155000, 240000],
                "employment_type": "Full-Time",
                "company_size": "5000-10000 Employees",
                "industry": "Transportation",
                "required_skills": ["Sketch", "Figma", "User Research", "Wireframing"],
                "values_promoted": ["Innovation", "Work-Life Balance"],
                "experience_required": "5-8 years",
                "role_level": "Senior"
            },
            {
                "job_id": "SLACK-555",
                "title": "UI/UX Designer",
                "company": "Slack",
                "location": "New York City",
                "salary_range": [130000, 190000],
                "employment_type": "Full-Time",
                "company_size": "501-1000 Employees",
                "industry": "Software",
                "required_skills": ["Figma", "UI/UX Design", "Prototyping"],
                "values_promoted": ["Transparency & Communication", "Mentorship & Career Development"],
                "experience_required": "3-5 years",
                "role_level": "Mid-level"
            },
            {
                "job_id": "NETFLIX-444",
                "title": "Senior UX Researcher",
                "company": "Netflix",
                "location": "Los Angeles, CA",
                "salary_range": [170000, 250000],
                "employment_type": "Full-Time",
                "company_size": "1000-5000 Employees",
                "industry": "Entertainment",
                "required_skills": ["User Research", "Data Analysis", "Prototyping"],
                "values_promoted": ["Innovation", "Impactful Work"],
                "experience_required": "6-9 years",
                "role_level": "Senior"
            },
            {
                "job_id": "SPOTIFY-333",
                "title": "Product Designer",
                "company": "Spotify",
                "location": "Remote in USA",
                "salary_range": [145000, 200000],
                "employment_type": "Full-Time",
                "company_size": "1000-5000 Employees",
                "industry": "Music & Audio",
                "required_skills": ["Figma", "UI/UX Design", "User Research"],
                "values_promoted": ["Work-Life Balance", "Innovation"],
                "experience_required": "4-7 years",
                "role_level": "Senior"
            },
            {
                "job_id": "TESLA-777",
                "title": "UX Designer",
                "company": "Tesla",
                "location": "Austin, TX",
                "salary_range": [120000, 180000],
                "employment_type": "Full-Time",
                "company_size": "5000-10000 Employees",
                "industry": "Automotive",
                "required_skills": ["Sketch", "Figma", "Wireframing"],
                "values_promoted": ["Innovation", "Impactful Work"],
                "experience_required": "2-5 years",
                "role_level": "Mid-level"
            },
            {
                "job_id": "MICROSOFT-888",
                "title": "Senior Design Lead",
                "company": "Microsoft",
                "location": "Seattle, WA",
                "salary_range": [190000, 290000],
                "employment_type": "Full-Time",
                "company_size": "10000+ Employees",
                "industry": "Technology",
                "required_skills": ["Design Leadership", "Figma", "Strategic Design"],
                "values_promoted": ["Mentorship & Career Development", "Innovation"],
                "experience_required": "8-12 years",
                "role_level": "Lead"
            },
            {
                "job_id": "ADOBE-999",
                "title": "UI Designer",
                "company": "Adobe",
                "location": "San Jose, CA",
                "salary_range": [125000, 175000],
                "employment_type": "Full-Time",
                "company_size": "5000-10000 Employees",
                "industry": "Software",
                "required_skills": ["Adobe Creative Suite", "Figma", "UI/UX Design"],
                "values_promoted": ["Creativity", "Work-Life Balance"],
                "experience_required": "3-6 years",
                "role_level": "Mid-level"
            },
            {
                "job_id": "STRIPE-111",
                "title": "Product Designer",
                "company": "Stripe",
                "location": "Remote in USA",
                "salary_range": [165000, 230000],
                "employment_type": "Contract",
                "company_size": "1000-5000 Employees",
                "industry": "Fintech",
                "required_skills": ["Figma", "Prototyping", "User Research"],
                "values_promoted": ["Innovation", "Transparency & Communication"],
                "experience_required": "5-8 years",
                "role_level": "Senior"
            },
            {
                "job_id": "ZOOM-222",
                "title": "Senior Visual Designer",
                "company": "Zoom",
                "location": "San Jose, CA",
                "salary_range": [140000, 200000],
                "employment_type": "Full-Time",
                "company_size": "1000-5000 Employees",
                "industry": "Communication",
                "required_skills": ["Adobe Creative Suite", "Branding", "UI/UX Design"],
                "values_promoted": ["Work-Life Balance", "Global Impact"],
                "experience_required": "6-9 years",
                "role_level": "Senior"
            }
        ]
        
        self.logger.info(f"Loaded {len(sample_jobs)} sample jobs")
        return sample_jobs
    
    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """Return all available jobs"""
        return self._jobs.copy()
    
    def get_job_by_id(self, job_id: str) -> Dict[str, Any]:
        """Get a specific job by ID"""
        for job in self._jobs:
            if job.get('job_id') == job_id:
                return job.copy()
        return None
    
    def add_job(self, job: Dict[str, Any]) -> bool:
        """Add a new job to the database"""
        try:
            required_fields = ['job_id', 'title', 'company', 'location']
            for field in required_fields:
                if field not in job:
                    raise ValueError(f"Missing required field: {field}")
            
            # Check if job ID already exists
            if self.get_job_by_id(job['job_id']):
                raise ValueError(f"Job ID {job['job_id']} already exists")
            
            self._jobs.append(job)
            self.logger.info(f"Added job {job['job_id']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding job: {e}")
            return False
    
    def get_unique_values(self, field: str) -> List[str]:
        """Get unique values for a specific field across all jobs"""
        values = set()
        for job in self._jobs:
            value = job.get(field)
            if isinstance(value, list):
                values.update(value)
            elif value:
                values.add(value)
        return sorted(list(values))
