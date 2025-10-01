#!/usr/bin/env python3
"""
Test script for AI-Based Smart Allocation Engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.recommender import AIInternshipRecommender

def test_ai_recommender():
    """Test the AI recommendation engine"""
    print("🤖 Testing AI-Based Smart Allocation Engine...")
    
    # Initialize the recommender
    try:
        recommender = AIInternshipRecommender()
        print("✅ AI Recommender initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing recommender: {e}")
        return
    
    # Test candidate data
    test_candidate = {
        "skills": ["Python", "Machine Learning", "Data Analysis"],
        "education": "BTech",
        "sector": "Information Technology",
        "location": "Bangalore",
        "social_category": "General",
        "district_type": "Urban",
        "expected_stipend": 18000,
        "experience_months": 6,
        "certifications": ["Python Certification"],
        "cgpa": 8.5,
        "past_participation": False
    }
    
    print(f"\n📋 Test Candidate Profile:")
    for key, value in test_candidate.items():
        print(f"   {key}: {value}")
    
    # Get AI recommendations
    try:
        recommendations = recommender.get_ai_recommendations(test_candidate)
        print(f"\n🎯 AI Recommendations Found: {len(recommendations)}")
        
        for i, internship in enumerate(recommendations, 1):
            print(f"\n{i}. {internship['title']} at {internship['company']}")
            print(f"   AI Match Score: {internship.get('ai_match_score', 0):.1f}%")
            print(f"   Location: {internship['location']}")
            print(f"   Stipend: {internship['stipend']}")
            print(f"   Available Positions: {internship.get('available_positions', 'N/A')}")
            if internship.get('affirmative_action_priority', 0) > 0:
                print(f"   ✓ Affirmative Action Applied")
        
        print(f"\n✅ AI matching completed successfully!")
        
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_recommender()