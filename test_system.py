#!/usr/bin/env python3
"""
AI Career Guidance System - Test Suite
======================================

Comprehensive testing script for the Career Guidance System.
Validates all core functionalities and ML components.

Usage:
    python test_system.py
"""

import pandas as pd
import numpy as np
from app import CareerGuidanceSystem, CAREER_DATABASE, QUIZ_QUESTIONS
import json

def test_career_database():
    """Test career database integrity"""
    print("🧪 Testing Career Database...")
    
    required_fields = ['description', 'job_roles', 'salary_range', 'tools', 'required_traits', 'learning_resources']
    
    for career_name, career_info in CAREER_DATABASE.items():
        for field in required_fields:
            assert field in career_info, f"Missing {field} in {career_name}"
        
        # Test required_traits format
        assert isinstance(career_info['required_traits'], dict), f"Invalid traits format for {career_name}"
        for trait, value in career_info['required_traits'].items():
            assert 0 <= value <= 1, f"Invalid trait value for {trait} in {career_name}"
    
    print(f"✅ Validated {len(CAREER_DATABASE)} career profiles")

def test_quiz_questions():
    """Test quiz question structure"""
    print("🧪 Testing Quiz Questions...")
    
    required_fields = ['question', 'trait', 'type']
    trait_counts = {}
    
    for i, question in enumerate(QUIZ_QUESTIONS):
        for field in required_fields:
            assert field in question, f"Missing {field} in question {i+1}"
        
        assert question['type'] in ['slider', 'radio'], f"Invalid question type in question {i+1}"
        
        # Count traits
        trait = question['trait']
        trait_counts[trait] = trait_counts.get(trait, 0) + 1
    
    print(f"✅ Validated {len(QUIZ_QUESTIONS)} quiz questions")
    print(f"📊 Trait coverage: {len(trait_counts)} unique traits")

def test_guidance_system():
    """Test the main guidance system"""
    print("🧪 Testing Guidance System...")
    
    # Initialize system
    system = CareerGuidanceSystem()
    
    # Test ML model training
    assert system.df is not None, "Failed to load/create dataset"
    assert len(system.df) > 0, "Empty dataset"
    
    system.train_ml_model()
    assert system.ml_model is not None, "Failed to train ML model"
    
    print("✅ System initialization successful")

def test_career_matching():
    """Test career matching algorithm"""
    print("🧪 Testing Career Matching Algorithm...")
    
    system = CareerGuidanceSystem()
    
    # Test sample user scores
    test_scores = {
        'math': 4,
        'logical_thinking': 5,
        'creativity': 2,
        'tech_affinity': 5,
        'empathy': 2,
        'communication': 3,
        'leadership': 3,
        'analytical': 4,
        'patience': 3,
        'organization': 3
    }
    
    # Calculate matches
    career_scores = system.calculate_career_match(test_scores)
    
    assert len(career_scores) > 0, "No career matches calculated"
    assert all(0 <= score <= 1 for score in career_scores.values()), "Invalid score range"
    
    # Check if tech-oriented profile matches tech careers
    sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    top_career = sorted_careers[0][0]
    
    print(f"✅ Top recommendation for tech profile: {top_career}")
    assert top_career in ["Software Engineer", "Data Scientist"], "Unexpected recommendation for tech profile"

def test_personality_tags():
    """Test personality tag generation"""
    print("🧪 Testing Personality Tags...")
    
    system = CareerGuidanceSystem()
    
    test_cases = [
        ({'creativity': 5, 'math': 2, 'empathy': 3}, "Creative Thinker"),
        ({'logical_thinking': 5, 'creativity': 2, 'empathy': 2}, "Analytical Mind"),
        ({'empathy': 5, 'communication': 4, 'creativity': 2}, "People Person"),
        ({'leadership': 5, 'organization': 4, 'communication': 4}, "Natural Leader")
    ]
    
    for scores, expected_category in test_cases:
        tag = system.get_personality_tag(scores)
        print(f"   Scores {scores} → {tag}")
        assert tag is not None, "Failed to generate personality tag"
    
    print("✅ Personality tag generation working")

def test_data_persistence():
    """Test data saving functionality"""
    print("🧪 Testing Data Persistence...")
    
    system = CareerGuidanceSystem()
    
    # Test data
    user_info = {
        'name': 'Test User',
        'age': 25,
        'education': "Bachelor's Degree",
        'stream': 'Computer Science'
    }
    
    career_result = {
        'top_career': 'Software Engineer',
        'confidence': 85.5,
        'personality_tag': 'Tech Enthusiast'
    }
    
    test_scores = {
        'math': 4,
        'logical_thinking': 5,
        'creativity': 3,
        'tech_affinity': 5,
        'empathy': 2,
        'communication': 3,
        'leadership': 3,
        'analytical': 4,
        'patience': 3,
        'organization': 4
    }
    
    # Save results
    system.save_results(user_info, career_result, test_scores)
    
    # Verify file creation
    import os
    assert os.path.exists('results.csv'), "Results file not created"
    
    # Verify data integrity
    results_df = pd.read_csv('results.csv')
    assert len(results_df) > 0, "No data saved to results file"
    assert 'name' in results_df.columns, "Missing name column"
    assert 'recommended_career' in results_df.columns, "Missing career column"
    
    print("✅ Data persistence working correctly")

def test_sample_user_journey():
    """Simulate a complete user journey"""
    print("🧪 Testing Complete User Journey...")
    
    system = CareerGuidanceSystem()
    
    # Step 1: User info
    user_info = {
        'name': 'Jane Smith',
        'age': 22,
        'education': "Bachelor's Degree",
        'stream': 'Computer Science'
    }
    
    # Step 2: Quiz responses (tech-oriented profile)
    quiz_responses = {
        'math': 4,
        'logical_thinking': 5,
        'creativity': 3,
        'tech_affinity': 5,
        'empathy': 3,
        'communication': 4,
        'leadership': 3,
        'analytical': 4,
        'patience': 3,
        'organization': 4
    }
    
    # Step 3: Get recommendations
    career_scores = system.calculate_career_match(quiz_responses)
    sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    
    top_career = sorted_careers[0][0]
    confidence = sorted_careers[0][1] * 100
    personality_tag = system.get_personality_tag(quiz_responses)
    
    # Step 4: Validate results
    assert top_career in CAREER_DATABASE, "Invalid career recommendation"
    assert 0 <= confidence <= 100, "Invalid confidence score"
    assert personality_tag is not None, "No personality tag generated"
    
    print(f"   👤 User: {user_info['name']}")
    print(f"   🎯 Recommended Career: {top_career}")
    print(f"   📊 Confidence: {confidence:.1f}%")
    print(f"   🏷️  Personality: {personality_tag}")
    
    # Step 5: Save complete results
    career_result = {
        'top_career': top_career,
        'confidence': confidence,
        'personality_tag': personality_tag
    }
    
    system.save_results(user_info, career_result, quiz_responses)
    
    print("✅ Complete user journey successful")

def generate_test_report():
    """Generate a comprehensive test report"""
    print("\n📋 Test Report Generation...")
    
    system = CareerGuidanceSystem()
    
    report = {
        'system_info': {
            'total_careers': len(CAREER_DATABASE),
            'total_questions': len(QUIZ_QUESTIONS),
            'dataset_size': len(system.df) if system.df is not None else 0
        },
        'career_database': list(CAREER_DATABASE.keys()),
        'traits_assessed': list(set(q['trait'] for q in QUIZ_QUESTIONS)),
        'ml_model_status': 'Trained' if system.ml_model else 'Not Available'
    }
    
    print(f"📊 System contains {report['system_info']['total_careers']} career paths")
    print(f"📋 Assessment covers {len(report['traits_assessed'])} personality traits")
    print(f"🤖 ML Model Status: {report['ml_model_status']}")
    
    # Save report
    with open('test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("✅ Test report saved as 'test_report.json'")

def main():
    """Run all tests"""
    print("🎯 AI Career Guidance System - Test Suite")
    print("=" * 50)
    
    try:
        # Core functionality tests
        test_career_database()
        test_quiz_questions()
        test_guidance_system()
        test_career_matching()
        test_personality_tags()
        test_data_persistence()
        test_sample_user_journey()
        
        # Generate report
        generate_test_report()
        
        print("\n🎉 All Tests Passed Successfully!")
        print("✅ System is ready for deployment")
        print("🚀 Run 'streamlit run app.py' to start the application")
        
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)