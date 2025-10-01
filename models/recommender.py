import json
import os
from typing import List, Dict, Any
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
from datetime import datetime

class AIInternshipRecommender:
    """
    AI-Based Smart Allocation Engine for PM Internship Scheme
    Uses advanced ML algorithms with affirmative action considerations
    Optimized for lightweight deployment on platforms like Railway
    """
    
    def __init__(self):
        self.internships_data = self._load_internships_data()
        self.applications_data = self._load_applications_data()
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=500)  # Reduced for storage
        self.scaler = StandardScaler()
        self.ml_model = RandomForestRegressor(n_estimators=50, random_state=42)  # Lightweight model
        self.model_path = 'data/ai_model.pkl'
        self._prepare_data()
        self._load_or_train_model()
    
    def _load_internships_data(self) -> List[Dict]:
        """Load internship data from JSON file with enhanced fields for AI matching"""
        data_file = os.path.join('data', 'internships.json')
        
        if not os.path.exists(data_file):
            # Create sample data if file doesn't exist
            sample_data = self._create_enhanced_sample_data()
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
            return sample_data
        
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading internship data: {e}")
            return self._create_enhanced_sample_data()
    
    def _load_applications_data(self) -> List[Dict]:
        """Load application/matching history for ML training"""
        data_file = os.path.join('data', 'applications.json')
        
        if not os.path.exists(data_file):
            return []
        
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading application data: {e}")
            return []
    
    def _create_enhanced_sample_data(self) -> List[Dict]:
        """Create enhanced sample internship data for AI-based matching"""
        return [
            {
                "id": 1,
                "title": "Software Development Intern",
                "company": "TechCorp India",
                "sector": "Information Technology",
                "location": "Bangalore",
                "district": "Bangalore Urban",
                "state": "Karnataka",
                "duration": "6 months",
                "stipend": "₹15,000/month",
                "stipend_amount": 15000,
                "skills_required": ["Python", "JavaScript", "HTML", "CSS", "Problem Solving"],
                "education_required": ["BTech", "MCA", "BCA"],
                "description": "Work on web applications and mobile app development projects",
                "opportunities": 50,
                "filled_positions": 12,
                "rating": 4.5,
                "company_type": "Private",
                "work_mode": "Hybrid",
                "affirmative_action": {
                    "rural_quota": 15,
                    "sc_quota": 8,
                    "st_quota": 4,
                    "obc_quota": 12,
                    "pwd_quota": 3
                },
                "industry_capacity": 100,
                "difficulty_level": "Intermediate",
                "growth_potential": "High"
            },
            {
                "id": 2,
                "title": "Digital Marketing Intern",
                "company": "MarketForce",
                "sector": "Marketing",
                "location": "Mumbai",
                "district": "Mumbai Suburban",
                "state": "Maharashtra",
                "duration": "4 months",
                "stipend": "₹12,000/month",
                "stipend_amount": 12000,
                "skills_required": ["Social Media", "Content Creation", "Analytics", "Communication"],
                "education_required": ["MBA", "BBA", "BA", "BCom"],
                "description": "Manage social media campaigns and create digital content",
                "opportunities": 30,
                "filled_positions": 8,
                "rating": 4.2,
                "company_type": "Private",
                "work_mode": "Hybrid",
                "affirmative_action": {
                    "rural_quota": 12,
                    "sc_quota": 6,
                    "st_quota": 3,
                    "obc_quota": 9,
                    "pwd_quota": 2
                },
                "industry_capacity": 80,
                "difficulty_level": "Beginner",
                "growth_potential": "Medium"
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
        """Prepare data for AI-based recommendations"""
        if not self.internships_data:
            return
        
        # Create feature text for each internship
        feature_texts = []
        for internship in self.internships_data:
            text = f"{internship['title']} {internship['sector']} {' '.join(internship['skills_required'])} {internship['description']}"
            feature_texts.append(text)
        
        # Fit TF-IDF vectorizer (reduced features for storage efficiency)
        if feature_texts:
            self.internship_features = self.vectorizer.fit_transform(feature_texts)
        
        # Prepare numerical features for ML model
        self.internship_numerical_features = self._extract_numerical_features()
    
    def _extract_numerical_features(self) -> np.ndarray:
        """Extract numerical features from internship data for ML model"""
        features = []
        
        for internship in self.internships_data:
            feature_vector = [
                internship.get('stipend_amount', 0),
                len(internship.get('skills_required', [])),
                internship.get('opportunities', 0),
                internship.get('filled_positions', 0),
                internship.get('rating', 0),
                internship.get('industry_capacity', 0),
                # Encode categorical features as numbers
                1 if internship.get('work_mode') == 'Remote' else 0,
                1 if internship.get('difficulty_level') == 'Beginner' else (2 if internship.get('difficulty_level') == 'Intermediate' else 3),
                1 if internship.get('growth_potential') == 'High' else (0.5 if internship.get('growth_potential') == 'Medium' else 0)
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def _load_or_train_model(self):
        """Load existing AI model or train a new one"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    self.ml_model = model_data['model']
                    self.scaler = model_data['scaler']
                print("AI model loaded successfully")
                return
            except Exception as e:
                print(f"Error loading model: {e}")
        
        # Train new model if none exists or loading failed
        self._train_ai_model()
    
    def _train_ai_model(self):
        """Train the AI model with synthetic data for prototype"""
        # Generate synthetic training data for prototype
        X_train, y_train = self._generate_synthetic_training_data()
        
        if len(X_train) > 0:
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            
            # Train the model
            self.ml_model.fit(X_train_scaled, y_train)
            
            # Save the model
            os.makedirs('data', exist_ok=True)
            model_data = {
                'model': self.ml_model,
                'scaler': self.scaler,
                'trained_at': datetime.now().isoformat()
            }
            
            try:
                with open(self.model_path, 'wb') as f:
                    pickle.dump(model_data, f)
                print("AI model trained and saved successfully")
            except Exception as e:
                print(f"Error saving model: {e}")
    
    def _generate_synthetic_training_data(self):
        """Generate synthetic training data for prototype demonstration"""
        X = []
        y = []
        
        # Create synthetic user-internship interaction data
        for _ in range(1000):  # Generate 1000 synthetic interactions
            # Random candidate features
            candidate_features = [
                np.random.randint(10000, 30000),  # Expected stipend
                np.random.randint(1, 8),          # Number of skills
                np.random.randint(1, 5),          # Experience level (1-4)
                np.random.random(),               # Location preference match (0-1)
                np.random.random(),               # Sector interest match (0-1)
                np.random.randint(0, 2),          # Remote work preference
                np.random.randint(1, 4),          # Education level
                np.random.random()                # Skills match percentage
            ]
            
            # Random internship features (matching format)
            internship_idx = np.random.randint(0, len(self.internships_data))
            internship = self.internships_data[internship_idx]
            
            internship_features = [
                internship.get('stipend_amount', 15000),
                len(internship.get('skills_required', [])),
                internship.get('opportunities', 50),
                internship.get('rating', 4.0),
                1 if internship.get('work_mode') == 'Remote' else 0,
                internship.get('industry_capacity', 100)
            ]
            
            # Combine features
            combined_features = candidate_features + internship_features
            
            # Generate realistic match score based on feature similarity
            match_score = self._calculate_synthetic_match_score(candidate_features, internship_features)
            
            X.append(combined_features)
            y.append(match_score)
        
        return np.array(X), np.array(y)
    
    def _calculate_synthetic_match_score(self, candidate_features, internship_features):
        """Calculate synthetic match score for training data"""
        score = 0
        
        # Stipend compatibility (higher if internship stipend meets candidate expectation)
        if internship_features[0] >= candidate_features[0] * 0.8:
            score += 30
        
        # Skills compatibility
        skills_match = min(candidate_features[1], internship_features[1]) / max(candidate_features[1], internship_features[1])
        score += skills_match * 25
        
        # Experience level match
        exp_diff = abs(candidate_features[2] - 2)  # Assuming internship is intermediate level
        score += max(0, 20 - exp_diff * 5)
        
        # Location/remote preference match
        if candidate_features[5] == internship_features[4]:  # Remote preference match
            score += 15
        
        # Add some randomness for realistic variation
        score += np.random.normal(0, 5)
        
        return max(0, min(100, score))  # Ensure score is between 0-100
    
    def get_ai_recommendations(self, candidate_data: Dict[str, Any]) -> List[Dict]:
        """
        AI-Based Smart Allocation Engine for internship recommendations
        
        Args:
            candidate_data: Dict containing candidate information including:
                - skills: List of candidate skills
                - education: Education level
                - location: Preferred location
                - sector: Preferred sector
                - social_category: For affirmative action (SC/ST/OBC/General)
                - district_type: For rural quota (Rural/Urban)
                - past_participation: Boolean for previous internships
                
        Returns:
            List of AI-matched internships with match scores
        """
        
        # Step 1: Apply affirmative action filters
        eligible_internships = self._apply_affirmative_action_filters(candidate_data)
        
        # Step 2: Apply capacity constraints
        available_internships = self._check_capacity_constraints(eligible_internships)
        
        # Step 3: AI-based matching and scoring
        ai_scored_internships = self._ai_match_and_score(candidate_data, available_internships)
        
        # Step 4: Apply diversity and fairness adjustments
        final_recommendations = self._apply_diversity_adjustments(ai_scored_internships, candidate_data)
        
        # Step 5: Sort by AI match score and return top 5
        recommendations = sorted(final_recommendations, key=lambda x: x['ai_match_score'], reverse=True)[:5]
        
        return recommendations
    
    def _apply_affirmative_action_filters(self, candidate_data: Dict[str, Any]) -> List[Dict]:
        """Apply affirmative action policies for fair representation"""
        eligible_internships = []
        
        social_category = candidate_data.get('social_category', 'General')
        district_type = candidate_data.get('district_type', 'Urban')
        
        for internship in self.internships_data:
            affirmative_action = internship.get('affirmative_action', {})
            
            # Check if candidate is eligible under affirmative action
            is_eligible = True
            
            # Rural quota check
            if district_type == 'Rural':
                rural_quota = affirmative_action.get('rural_quota', 0)
                # Simulate current rural filled positions (for prototype)
                rural_filled = internship.get('filled_positions', 0) * 0.1  # Assume 10% are rural
                if rural_filled >= rural_quota:
                    # Still eligible through general quota
                    pass
            
            # Social category quota check
            category_quotas = {
                'SC': affirmative_action.get('sc_quota', 0),
                'ST': affirmative_action.get('st_quota', 0),
                'OBC': affirmative_action.get('obc_quota', 0)
            }
            
            if social_category in category_quotas:
                # Add priority scoring for reserved categories
                internship_copy = internship.copy()
                internship_copy['affirmative_action_priority'] = 10
                eligible_internships.append(internship_copy)
            else:
                # General category
                internship_copy = internship.copy()
                internship_copy['affirmative_action_priority'] = 0
                eligible_internships.append(internship_copy)
        
        return eligible_internships
    
    def _check_capacity_constraints(self, internships: List[Dict]) -> List[Dict]:
        """Filter internships based on available capacity"""
        available_internships = []
        
        for internship in internships:
            total_capacity = internship.get('opportunities', 0)
            filled_positions = internship.get('filled_positions', 0)
            
            if filled_positions < total_capacity:
                internship_copy = internship.copy()
                internship_copy['available_positions'] = total_capacity - filled_positions
                internship_copy['capacity_utilization'] = (filled_positions / total_capacity) * 100 if total_capacity > 0 else 0
                available_internships.append(internship_copy)
        
        return available_internships
    
    def _ai_match_and_score(self, candidate_data: Dict[str, Any], internships: List[Dict]) -> List[Dict]:
        """Use AI model to score internship matches"""
        if not internships:
            return []
        
        scored_internships = []
        
        for internship in internships:
            # Extract candidate features for AI model
            candidate_features = self._extract_candidate_features(candidate_data)
            internship_features = self._extract_internship_features_for_ai(internship)
            
            # Combine features for AI prediction
            combined_features = np.array([candidate_features + internship_features])
            
            try:
                # Scale features and predict match score
                scaled_features = self.scaler.transform(combined_features)
                ai_score = self.ml_model.predict(scaled_features)[0]
                
                # Combine with rule-based scoring for robustness
                rule_score = self._calculate_rule_based_score(candidate_data, internship)
                
                # Weighted combination: 70% AI, 30% rules
                final_score = (ai_score * 0.7) + (rule_score * 0.3)
                
                # Add affirmative action bonus
                aa_bonus = internship.get('affirmative_action_priority', 0)
                final_score += aa_bonus
                
                internship_copy = internship.copy()
                internship_copy['ai_match_score'] = min(100, max(0, final_score))
                internship_copy['ai_raw_score'] = ai_score
                internship_copy['rule_score'] = rule_score
                scored_internships.append(internship_copy)
                
            except Exception as e:
                # Fallback to rule-based scoring
                rule_score = self._calculate_rule_based_score(candidate_data, internship)
                internship_copy = internship.copy()
                internship_copy['ai_match_score'] = rule_score
                internship_copy['ai_raw_score'] = 0
                internship_copy['rule_score'] = rule_score
                scored_internships.append(internship_copy)
        
        return scored_internships
    
    def _extract_candidate_features(self, candidate_data: Dict[str, Any]) -> List[float]:
        """Extract numerical features from candidate data for AI model"""
        skills = candidate_data.get('skills', [])
        education = candidate_data.get('education', '')
        
        # Map education to numeric value
        education_mapping = {'BTech': 4, 'MTech': 5, 'MBA': 5, 'MSc': 5, 'BCA': 3, 'MCA': 4, 'BCom': 3, 'BA': 3, 'BSc': 3}
        education_level = education_mapping.get(education, 3)
        
        features = [
            candidate_data.get('expected_stipend', 15000),  # Expected stipend
            len(skills),                                    # Number of skills
            education_level,                               # Education level
            1 if candidate_data.get('location', '').lower() in ['remote', 'anywhere'] else 0,  # Remote preference
            candidate_data.get('experience_months', 0),    # Experience in months
            1 if candidate_data.get('district_type') == 'Rural' else 0,  # Rural background
            len(candidate_data.get('certifications', [])), # Number of certifications
            candidate_data.get('cgpa', 7.0)               # Academic performance
        ]
        
        return features
    
    def _extract_internship_features_for_ai(self, internship: Dict[str, Any]) -> List[float]:
        """Extract numerical features from internship data for AI model"""
        features = [
            internship.get('stipend_amount', 15000),
            len(internship.get('skills_required', [])),
            internship.get('available_positions', 10),
            internship.get('rating', 4.0),
            1 if internship.get('work_mode') == 'Remote' else 0,
            internship.get('industry_capacity', 100)
        ]
        
        return features
    
    def _calculate_rule_based_score(self, candidate_data: Dict[str, Any], internship: Dict[str, Any]) -> float:
        """Calculate rule-based compatibility score"""
        score = 0
        
        # Skills matching
        candidate_skills = [skill.lower() for skill in candidate_data.get('skills', [])]
        required_skills = [skill.lower() for skill in internship.get('skills_required', [])]
        
        skill_matches = sum(1 for skill in candidate_skills if any(skill in req or req in skill for req in required_skills))
        if required_skills:
            skill_score = (skill_matches / len(required_skills)) * 40
            score += skill_score
        
        # Education matching
        candidate_education = candidate_data.get('education', '').lower()
        required_education = [edu.lower() for edu in internship.get('education_required', [])]
        if any(edu in candidate_education or candidate_education in edu for edu in required_education) or 'any' in required_education:
            score += 25
        
        # Location preference
        candidate_location = candidate_data.get('location', '').lower()
        internship_location = internship.get('location', '').lower()
        if (candidate_location in internship_location or internship_location in candidate_location or 
            internship_location == 'remote' or candidate_location == 'anywhere'):
            score += 20
        
        # Sector interest
        candidate_sector = candidate_data.get('sector', '').lower()
        internship_sector = internship.get('sector', '').lower()
        if candidate_sector in internship_sector or internship_sector in candidate_sector:
            score += 15
        
        return min(100, score)
    
    def _apply_diversity_adjustments(self, scored_internships: List[Dict], candidate_data: Dict[str, Any]) -> List[Dict]:
        """Apply diversity and fairness adjustments to recommendations"""
        # Ensure diversity in sectors and companies
        final_recommendations = []
        seen_sectors = set()
        seen_companies = set()
        
        # Sort by score first
        sorted_internships = sorted(scored_internships, key=lambda x: x['ai_match_score'], reverse=True)
        
        # Add top recommendations while maintaining diversity
        for internship in sorted_internships:
            sector = internship.get('sector', '')
            company = internship.get('company', '')
            
            # Prioritize diversity (max 2 per sector, 1 per company)
            if len(final_recommendations) < 5:
                if (sector not in seen_sectors or len([r for r in final_recommendations if r.get('sector') == sector]) < 2) and \
                   company not in seen_companies:
                    final_recommendations.append(internship)
                    seen_sectors.add(sector)
                    seen_companies.add(company)
        
        # Fill remaining slots if needed
        while len(final_recommendations) < 5 and len(final_recommendations) < len(sorted_internships):
            for internship in sorted_internships:
                if internship not in final_recommendations:
                    final_recommendations.append(internship)
                    break
        
        return final_recommendations
    
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
    
    # Legacy method for backward compatibility
    def get_recommendations(self, candidate_data: Dict[str, Any]) -> List[Dict]:
        """Legacy method - redirects to AI recommendations"""
        return self.get_ai_recommendations(candidate_data)
    
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