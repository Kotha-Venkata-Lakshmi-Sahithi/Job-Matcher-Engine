import re
import math
from typing import Dict, List, Any, Tuple
import logging

class JobRecommendationEngine:
    """
    Job recommendation engine that matches candidate preferences with job listings
    using weighted scoring algorithms.
    """
    
    # Default weights for matching criteria
    DEFAULT_WEIGHTS = {
        'skills': 0.30,      # 30%
        'title': 0.20,       # 20%
        'location': 0.15,    # 15%
        'industry': 0.10,    # 10%
        'company_size': 0.10, # 10%
        'values': 0.10,      # 10%
        'salary': 0.05       # 5%
    }
    
    # Semantic matching for job titles
    TITLE_SYNONYMS = {
        'ux designer': ['user experience designer', 'product designer', 'interaction designer'],
        'ui designer': ['user interface designer', 'visual designer', 'product designer'],
        'product designer': ['ux designer', 'ui designer', 'user experience designer'],
        'senior ux designer': ['senior product designer', 'lead ux designer'],
        'frontend developer': ['front-end developer', 'ui developer', 'web developer'],
        'backend developer': ['back-end developer', 'server-side developer'],
        'full stack developer': ['fullstack developer', 'full-stack developer'],
        'data scientist': ['machine learning engineer', 'data analyst'],
        'software engineer': ['software developer', 'programmer'],
        'design manager': ['design lead', 'head of design'],
        'engineering manager': ['engineering lead', 'tech lead']
    }
    
    def __init__(self, job_database):
        self.job_db = job_database
        self.weights = self.DEFAULT_WEIGHTS.copy()
        self.logger = logging.getLogger(__name__)
    
    def set_weights(self, weights: Dict[str, float]):
        """Update the weights for matching criteria"""
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total_weight}")
        self.weights.update(weights)
    
    def recommend_jobs(self, preferences: Dict[str, Any], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Generate job recommendations based on candidate preferences
        
        Args:
            preferences: Dictionary containing candidate job preferences
            limit: Maximum number of recommendations to return
            
        Returns:
            List of job recommendations with match scores
        """
        try:
            jobs = self.job_db.get_all_jobs()
            self.logger.debug(f"Evaluating {len(jobs)} jobs against preferences")
            
            if not jobs:
                self.logger.warning("No jobs available in database")
                return []
            
            scored_jobs = []
            
            for job in jobs:
                try:
                    match_score, breakdown = self._calculate_match_score(preferences, job)
                    
                    if match_score > 0:  # Only include jobs with some match
                        scored_jobs.append({
                            'job_id': job.get('job_id'),
                            'job_title': job.get('title'),
                            'company': job.get('company'),
                            'location': job.get('location'),
                            'salary_range': job.get('salary_range'),
                            'employment_type': job.get('employment_type'),
                            'match_score': round(match_score),
                            'breakdown': breakdown,
                            'job_details': job
                        })
                except Exception as e:
                    self.logger.error(f"Error scoring job {job.get('job_id', 'unknown')}: {e}")
                    continue
            
            # Sort by match score (descending) and limit results
            scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)
            
            self.logger.debug(f"Generated {len(scored_jobs)} scored recommendations")
            return scored_jobs[:limit]
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            raise
    
    def _calculate_match_score(self, preferences: Dict[str, Any], job: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """
        Calculate match score between preferences and job
        
        Returns:
            Tuple of (total_match_score, score_breakdown)
        """
        breakdown = {}
        total_score = 0.0
        
        # Skills matching (30%)
        skills_score = self._match_skills(preferences.get('skills', []), job.get('required_skills', []))
        breakdown['skills'] = skills_score
        total_score += skills_score * self.weights['skills']
        
        # Title/Role matching (20%)
        title_score = self._match_titles(preferences.get('titles', []), job.get('title', ''))
        breakdown['title'] = title_score
        total_score += title_score * self.weights['title']
        
        # Location matching (15%)
        location_score = self._match_locations(preferences.get('locations', []), job.get('location', ''))
        breakdown['location'] = location_score
        total_score += location_score * self.weights['location']
        
        # Industry matching (10%)
        industry_score = self._match_industries(preferences.get('industries', []), job.get('industry', ''))
        breakdown['industry'] = industry_score
        total_score += industry_score * self.weights['industry']
        
        # Company size matching (10%)
        size_score = self._match_company_size(preferences.get('company_size', []), job.get('company_size', ''))
        breakdown['company_size'] = size_score
        total_score += size_score * self.weights['company_size']
        
        # Values matching (10%)
        values_score = self._match_values(preferences.get('values', []), job.get('values_promoted', []))
        breakdown['values'] = values_score
        total_score += values_score * self.weights['values']
        
        # Salary matching (5%)
        salary_score = self._match_salary(preferences.get('min_salary', 0), job.get('salary_range', []))
        breakdown['salary'] = salary_score
        total_score += salary_score * self.weights['salary']
        
        # Convert to 0-100 scale
        return total_score * 100, {k: round(v * 100) for k, v in breakdown.items()}
    
    def _match_skills(self, preferred_skills: List[str], job_skills: List[str]) -> float:
        """Match skills with partial scoring for similar skills"""
        if not preferred_skills:
            return 0.5  # Neutral score if no preference
        if not job_skills:
            return 0.0
        
        preferred_lower = [skill.lower().strip() for skill in preferred_skills]
        job_skills_lower = [skill.lower().strip() for skill in job_skills]
        
        matches = 0
        for pref_skill in preferred_lower:
            # Exact match
            if pref_skill in job_skills_lower:
                matches += 1
            else:
                # Partial match (contains)
                for job_skill in job_skills_lower:
                    if pref_skill in job_skill or job_skill in pref_skill:
                        matches += 0.7
                        break
        
        return min(matches / len(preferred_skills), 1.0)
    
    def _match_titles(self, preferred_titles: List[str], job_title: str) -> float:
        """Match job titles with semantic similarity"""
        if not preferred_titles:
            return 0.5
        if not job_title:
            return 0.0
        
        job_title_lower = job_title.lower().strip()
        best_match = 0.0
        
        for pref_title in preferred_titles:
            pref_title_lower = pref_title.lower().strip()
            
            # Exact match
            if pref_title_lower == job_title_lower:
                return 1.0
            
            # Semantic matching using synonyms
            match_score = self._semantic_title_match(pref_title_lower, job_title_lower)
            best_match = max(best_match, match_score)
            
            # Partial string matching
            if pref_title_lower in job_title_lower or job_title_lower in pref_title_lower:
                best_match = max(best_match, 0.8)
        
        return best_match
    
    def _semantic_title_match(self, pref_title: str, job_title: str) -> float:
        """Check semantic similarity between job titles"""
        # Check if either title has synonyms that match the other
        pref_synonyms = self.TITLE_SYNONYMS.get(pref_title, [])
        job_synonyms = self.TITLE_SYNONYMS.get(job_title, [])
        
        # Check if job title is a synonym of preferred title
        if job_title in pref_synonyms:
            return 0.9
        
        # Check if preferred title is a synonym of job title
        if pref_title in job_synonyms:
            return 0.9
        
        # Check for overlapping synonyms
        for synonym in pref_synonyms:
            if synonym in job_synonyms:
                return 0.8
        
        return 0.0
    
    def _match_locations(self, preferred_locations: List[str], job_location: str) -> float:
        """Match job locations"""
        if not preferred_locations:
            return 0.5
        if not job_location:
            return 0.0
        
        job_location_lower = job_location.lower().strip()
        
        for pref_location in preferred_locations:
            pref_location_lower = pref_location.lower().strip()
            
            # Exact match
            if pref_location_lower == job_location_lower:
                return 1.0
            
            # Remote matching
            if 'remote' in pref_location_lower and 'remote' in job_location_lower:
                return 1.0
            
            # City/state partial matching
            if pref_location_lower in job_location_lower or job_location_lower in pref_location_lower:
                return 0.8
        
        return 0.0
    
    def _match_industries(self, preferred_industries: List[str], job_industry: str) -> float:
        """Match industries"""
        if not preferred_industries:
            return 0.5
        if not job_industry:
            return 0.0
        
        job_industry_lower = job_industry.lower().strip()
        
        for pref_industry in preferred_industries:
            pref_industry_lower = pref_industry.lower().strip()
            
            if pref_industry_lower == job_industry_lower:
                return 1.0
            
            # Partial match for related industries
            if pref_industry_lower in job_industry_lower or job_industry_lower in pref_industry_lower:
                return 0.7
        
        return 0.0
    
    def _match_company_size(self, preferred_sizes: List[str], job_size: str) -> float:
        """Match company sizes"""
        if not preferred_sizes:
            return 0.5
        if not job_size:
            return 0.0
        
        job_size_lower = job_size.lower().strip()
        
        for pref_size in preferred_sizes:
            pref_size_lower = pref_size.lower().strip()
            
            if pref_size_lower == job_size_lower:
                return 1.0
        
        return 0.0
    
    def _match_values(self, preferred_values: List[str], job_values: List[str]) -> float:
        """Match company values"""
        if not preferred_values:
            return 0.5
        if not job_values:
            return 0.0
        
        preferred_lower = [val.lower().strip() for val in preferred_values]
        job_values_lower = [val.lower().strip() for val in job_values]
        
        matches = 0
        for pref_val in preferred_lower:
            if pref_val in job_values_lower:
                matches += 1
        
        return matches / len(preferred_values)
    
    def _match_salary(self, min_salary: int, job_salary_range: List[int]) -> float:
        """Match salary requirements"""
        if not min_salary:
            return 1.0  # No salary preference
        if not job_salary_range or len(job_salary_range) != 2:
            return 0.0
        
        job_min, job_max = job_salary_range
        
        # Perfect match if min salary is within range
        if job_min <= min_salary <= job_max:
            return 1.0
        
        # Partial match if close to range
        if min_salary < job_min:
            gap = job_min - min_salary
            if gap <= 20000:  # Within 20k
                return 0.8
        
        if min_salary > job_max:
            gap = min_salary - job_max
            if gap <= 20000:  # Within 20k
                return 0.6
        
        return 0.0
