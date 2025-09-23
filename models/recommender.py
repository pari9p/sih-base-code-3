import json
import os
from typing import List, Dict, Any
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class InternshipRecommender:
    """
    Lightweight recommendation engine for PM Internship Scheme
    Uses rule-based matching and basic ML techniques for recommendations
    """
    
    def __init__(self):
        self.internships_data = self._load_internships_data()
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self._prepare_data()
    
    def _load_internships_data(self) -> List[Dict]:
        """Load internship data from JSON file"""
        data_file = os.path.join('data', 'internships.json')
        
        if not os.path.exists(data_file):
            # Create sample data if file doesn't exist
            sample_data = self._create_sample_data()
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
            return sample_data
        
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading internship data: {e}")
            return self._create_sample_data()
    
    def _create_sample_data(self) -> List[Dict]:
        """Create sample internship data for demonstration"""
        return [
            {
                "id": 1,
                "title": "Software Development Intern",
                "company": "TechCorp India",
                "sector": "Information Technology",
                "location": "Bangalore",
                "duration": "6 months",
                "stipend": "₹15,000/month",
                "skills_required": ["Python", "JavaScript", "HTML", "CSS", "Problem Solving"],
                "education_required": ["BTech", "MCA", "BCA"],
                "description": "Work on web applications and mobile app development projects",
                "opportunities": 50,
                "rating": 4.5
            },
            {
                "id": 2,
                "title": "Digital Marketing Intern",
                "company": "MarketForce",
                "sector": "Marketing",
                "location": "Mumbai",
                "duration": "4 months",
                "stipend": "₹12,000/month",
                "skills_required": ["Social Media", "Content Creation", "Analytics", "Communication"],
                "education_required": ["MBA", "BBA", "BA", "BCom"],
                "description": "Manage social media campaigns and create digital content",
                "opportunities": 30,
                "rating": 4.2
            },
            {
                "id": 3,
                "title": "Data Analysis Intern",
                "company": "DataInsights Ltd",
                "sector": "Analytics",
                "location": "Delhi",
                "duration": "6 months",
                "stipend": "₹18,000/month",
                "skills_required": ["Excel", "Python", "SQL", "Statistics", "Data Visualization"],
                "education_required": ["BTech", "MSc", "BSc", "BCA"],
                "description": "Analyze business data and create reports for decision making",
                "opportunities": 25,
                "rating": 4.7
            },
            {
                "id": 4,
                "title": "Content Writing Intern",
                "company": "ContentCrafters",
                "sector": "Media",
                "location": "Remote",
                "duration": "3 months",
                "stipend": "₹8,000/month",
                "skills_required": ["Writing", "Research", "Creativity", "Communication"],
                "education_required": ["BA", "MA", "BJournalism", "English"],
                "description": "Create engaging content for websites and social media",
                "opportunities": 40,
                "rating": 4.0
            },
            {
                "id": 5,
                "title": "Finance Intern",
                "company": "FinanceHub",
                "sector": "Finance",
                "location": "Chennai",
                "duration": "6 months",
                "stipend": "₹14,000/month",
                "skills_required": ["Excel", "Financial Analysis", "Accounting", "Mathematics"],
                "education_required": ["BCom", "MBA", "CA", "BBA"],
                "description": "Support financial planning and analysis activities",
                "opportunities": 20,
                "rating": 4.3
            },
            {
                "id": 6,
                "title": "Graphic Design Intern",
                "company": "CreativeStudio",
                "sector": "Design",
                "location": "Pune",
                "duration": "4 months",
                "stipend": "₹10,000/month",
                "skills_required": ["Photoshop", "Illustrator", "Creativity", "Design Thinking"],
                "education_required": ["BFA", "BDes", "Diploma", "Any"],
                "description": "Design graphics for marketing materials and digital media",
                "opportunities": 15,
                "rating": 4.1
            },
            {
                "id": 7,
                "title": "HR Intern",
                "company": "PeopleFirst",
                "sector": "Human Resources",
                "location": "Hyderabad",
                "duration": "5 months",
                "stipend": "₹11,000/month",
                "skills_required": ["Communication", "Interpersonal", "Organization", "MS Office"],
                "education_required": ["MBA", "BBA", "BA", "Any"],
                "description": "Support recruitment, employee engagement and HR operations",
                "opportunities": 35,
                "rating": 4.4
            },
            {
                "id": 8,
                "title": "Research Intern",
                "company": "ResearchLab India",
                "sector": "Research",
                "location": "Kolkata",
                "duration": "6 months",
                "stipend": "₹16,000/month",
                "skills_required": ["Research", "Analysis", "Writing", "Critical Thinking"],
                "education_required": ["MSc", "MA", "PhD", "BTech"],
                "description": "Conduct research projects and prepare detailed reports",
                "opportunities": 12,
                "rating": 4.6
            },
            {
                "id": 9,
                "title": "Sales Intern",
                "company": "SalesForce India",
                "sector": "Sales",
                "location": "Ahmedabad",
                "duration": "4 months",
                "stipend": "₹9,000/month + Incentives",
                "skills_required": ["Communication", "Persuasion", "Customer Service", "Networking"],
                "education_required": ["Any", "BBA", "BCom", "MBA"],
                "description": "Support sales team and learn customer relationship management",
                "opportunities": 45,
                "rating": 3.9
            },
            {
                "id": 10,
                "title": "Teaching Assistant",
                "company": "EduTech Solutions",
                "sector": "Education",
                "location": "Jaipur",
                "duration": "5 months",
                "stipend": "₹13,000/month",
                "skills_required": ["Teaching", "Subject Knowledge", "Patience", "Communication"],
                "education_required": ["BTech", "MSc", "MA", "BEd"],
                "description": "Assist in teaching and curriculum development activities",
                "opportunities": 25,
                "rating": 4.3
            }
        ]
    
    def _prepare_data(self):
        """Prepare data for ML-based recommendations"""
        if not self.internships_data:
            return
        
        # Create feature text for each internship
        feature_texts = []
        for internship in self.internships_data:
            text = f"{internship['title']} {internship['sector']} {' '.join(internship['skills_required'])} {internship['description']}"
            feature_texts.append(text)
        
        # Fit TF-IDF vectorizer
        if feature_texts:
            self.internship_features = self.vectorizer.fit_transform(feature_texts)
    
    def get_recommendations(self, candidate_data: Dict[str, Any]) -> List[Dict]:
        """
        Get top 3-5 internship recommendations for a candidate
        
        Args:
            candidate_data: Dict containing candidate information
            
        Returns:
            List of recommended internships
        """
        # PROTOTYPE: Add hardcoded recommendations at the top
        hardcoded_recommendations = [
            {
                "id": 999,
                "title": "AI/ML Intern (Premium)",
                "company": "FutureTech Solutions",
                "sector": "Artificial Intelligence",
                "location": "Bangalore",
                "duration": "6 months",
                "stipend": "₹25,000/month",
                "skills_required": ["Python", "Machine Learning", "TensorFlow", "Data Science"],
                "education_required": ["BTech", "MTech", "MSc"],
                "description": "Work on cutting-edge AI projects and machine learning models",
                "opportunities": 5,
                "rating": 4.9,
                "match_score": 100
            },
            {
                "id": 998,
                "title": "Full Stack Developer (Featured)",
                "company": "InnovateLab",
                "sector": "Information Technology",
                "location": "Mumbai",
                "duration": "8 months",
                "stipend": "₹22,000/month",
                "skills_required": ["React", "Node.js", "MongoDB", "JavaScript"],
                "education_required": ["BTech", "BCA", "MCA"],
                "description": "Build modern web applications using latest technologies",
                "opportunities": 8,
                "rating": 4.8,
                "match_score": 95
            }
        ]
        
        # Rule-based filtering
        filtered_internships = self._apply_rules(candidate_data)
        
        # ML-based scoring for filtered internships
        scored_internships = self._score_with_ml(candidate_data, filtered_internships)
        
        # Sort by score and return top recommendations (excluding space for hardcoded ones)
        recommendations = sorted(scored_internships, key=lambda x: x['match_score'], reverse=True)[:3]
        
        # Combine hardcoded recommendations with regular ones
        final_recommendations = hardcoded_recommendations + recommendations
        
        # Ensure at least 5 recommendations total
        if len(final_recommendations) < 5:
            # Fill with additional recommendations if needed
            all_scored = self._score_with_ml(candidate_data, self.internships_data)
            all_sorted = sorted(all_scored, key=lambda x: x['match_score'], reverse=True)
            
            # Add recommendations not already included
            existing_ids = {rec['id'] for rec in final_recommendations}
            for internship in all_sorted:
                if internship['id'] not in existing_ids and len(final_recommendations) < 5:
                    final_recommendations.append(internship)
        
        return final_recommendations[:5]  # Return maximum 5 recommendations
    
    def _apply_rules(self, candidate_data: Dict[str, Any]) -> List[Dict]:
        """Apply rule-based filtering"""
        filtered = []
        
        candidate_education = candidate_data.get('education', '').lower()
        candidate_skills = [skill.lower().strip() for skill in candidate_data.get('skills', [])]
        candidate_sector = candidate_data.get('sector', '').lower()
        candidate_location = candidate_data.get('location', '').lower()
        
        for internship in self.internships_data:
            score = 0
            
            # Education matching
            education_required = [edu.lower() for edu in internship.get('education_required', [])]
            if any(edu in candidate_education or candidate_education in edu for edu in education_required) or 'any' in education_required:
                score += 3
            
            # Skills matching
            skills_required = [skill.lower() for skill in internship.get('skills_required', [])]
            skill_matches = sum(1 for skill in candidate_skills 
                              if any(skill in req_skill or req_skill in skill for req_skill in skills_required))
            score += skill_matches * 2
            
            # Sector matching
            if candidate_sector in internship.get('sector', '').lower():
                score += 4
            
            # Location preference (remote gets bonus for any location)
            internship_location = internship.get('location', '').lower()
            if (candidate_location in internship_location or 
                internship_location in candidate_location or
                internship_location == 'remote'):
                score += 2
            
            # Add internship with score
            if score > 0:  # Only include if there's some match
                internship_copy = internship.copy()
                internship_copy['rule_score'] = score
                filtered.append(internship_copy)
        
        return filtered
    
    def _score_with_ml(self, candidate_data: Dict[str, Any], internships: List[Dict]) -> List[Dict]:
        """Score internships using ML similarity"""
        if not hasattr(self, 'internship_features') or not internships:
            # Fallback to rule-based scoring only
            for internship in internships:
                internship['match_score'] = internship.get('rule_score', 0)
            return internships
        
        try:
            # Create candidate feature vector
            candidate_text = f"{candidate_data.get('education', '')} {candidate_data.get('sector', '')} {' '.join(candidate_data.get('skills', []))}"
            candidate_vector = self.vectorizer.transform([candidate_text])
            
            scored_internships = []
            for internship in internships:
                # Find the internship in original data to get its feature index
                internship_idx = None
                for idx, original in enumerate(self.internships_data):
                    if original['id'] == internship['id']:
                        internship_idx = idx
                        break
                
                if internship_idx is not None:
                    # Calculate similarity
                    similarity = cosine_similarity(candidate_vector, 
                                                 self.internship_features[internship_idx:internship_idx+1])[0][0]
                    
                    # Combine rule-based score with ML similarity
                    rule_score = internship.get('rule_score', 0)
                    ml_score = similarity * 10  # Scale similarity to 0-10
                    combined_score = rule_score + ml_score
                    
                    internship_copy = internship.copy()
                    internship_copy['match_score'] = combined_score
                    scored_internships.append(internship_copy)
                else:
                    # Fallback to rule score only
                    internship_copy = internship.copy()
                    internship_copy['match_score'] = internship.get('rule_score', 0)
                    scored_internships.append(internship_copy)
            
            return scored_internships
            
        except Exception as e:
            print(f"ML scoring error: {e}")
            # Fallback to rule-based scoring
            for internship in internships:
                internship['match_score'] = internship.get('rule_score', 0)
            return internships
    
    def get_available_sectors(self) -> List[str]:
        """Get list of available sectors"""
        sectors = set()
        for internship in self.internships_data:
            sectors.add(internship.get('sector', ''))
        return sorted(list(sectors))
    
    def get_available_locations(self) -> List[str]:
        """Get list of available locations"""
        locations = set()
        for internship in self.internships_data:
            location = internship.get('location', '')
            if location:
                locations.add(location)
        return sorted(list(locations))