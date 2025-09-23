#!/usr/bin/env python3
"""
Test script for the streamlined PM Internship recommendation system
"""

from models.recommender import InternshipRecommender

def test_recommendations():
    recommender = InternshipRecommender()
    
    # Test candidate data
    candidate_data = {
        'education': 'BTech',
        'skills': ['Python', 'JavaScript', 'Web Development'],
        'sector': 'Information Technology',
        'location': 'Bangalore'
    }
    
    print("Testing PM Internship Recommendation System")
    print("=" * 50)
    print(f"Candidate: {candidate_data}")
    print("\nRecommendations:")
    print("-" * 30)
    
    recommendations = recommender.get_recommendations(candidate_data)
    
    for i, internship in enumerate(recommendations, 1):
        print(f"\n{i}. {internship['title']} at {internship['company']}")
        print(f"   Sector: {internship['sector']} | Location: {internship['location']}")
        print(f"   Stipend: {internship['stipend']} | Duration: {internship['duration']}")
        print(f"   Match Score: {internship['match_score']:.2f}")
        print(f"   Skills: {', '.join(internship['skills_required'])}")
    
    print(f"\nTotal recommendations: {len(recommendations)}")
    
    # Check if hardcoded recommendations are present
    hardcoded_ids = [999, 998]
    hardcoded_found = [r for r in recommendations if r['id'] in hardcoded_ids]
    print(f"Hardcoded recommendations found: {len(hardcoded_found)}/2")
    
    for rec in hardcoded_found:
        print(f"  - {rec['title']} (ID: {rec['id']})")

if __name__ == "__main__":
    test_recommendations()