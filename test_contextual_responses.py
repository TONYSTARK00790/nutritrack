"""
Test to verify the chatbot responds contextually to different questions
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from accounts.enhanced_chatbot import SmartNutritionChatbot

# Create test user
user, _ = User.objects.get_or_create(username='response_test', defaults={'email': 'test@test.com'})
profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'goal': 'Gain Muscle'})

# Initialize bot
bot = SmartNutritionChatbot(user)

# Test cases
test_cases = [
    {
        "question": "How much protein should I eat for muscle?",
        "expected_keywords": ["protein", "0.7", "1g"],
        "category": "Nutrition - Protein"
    },
    {
        "question": "How do I do squats properly?",
        "expected_keywords": ["squat", "form", "beginner", "reps"],
        "category": "Fitness - Squats"
    },
    {
        "question": "I'm feeling really tired all the time",
        "expected_keywords": ["energy", "sleep", "hydration"],
        "category": "Health - Fatigue"
    },
    {
        "question": "What's the best cardio for weight loss?",
        "expected_keywords": ["cardio", "zone", "fat loss"],
        "category": "Fitness - Cardio"
    },
    {
        "question": "How much water should I drink?",
        "expected_keywords": ["hydration", "half bodyweight", "ounces"],
        "category": "Nutrition - Hydration"
    },
]

print("\n" + "="*80)
print("TESTING CHATBOT CONTEXTUAL RESPONSES")
print("="*80)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n[Test {i}] {test_case['category']}")
    print(f"Question: {test_case['question']}")
    
    # Get response
    response = bot.get_response(test_case['question'])
    
    # Check if expected keywords are in response
    found_keywords = [kw for kw in test_case['expected_keywords'] if kw.lower() in response.lower()]
    
    print(f"Response: {response[:120]}...")
    print(f"Length: {len(response)} chars")
    
    # Check for topic detection
    sentiment = bot.analyze_sentiment(test_case['question'])
    print(f"Detected Topics: {sentiment['topics']}")
    
    if found_keywords:
        print(f"[OK] Found {len(found_keywords)}/{len(test_case['expected_keywords'])} expected keywords: {found_keywords}")
    else:
        print(f"[WARN] No expected keywords found. Expected: {test_case['expected_keywords']}")
    
    print("-" * 80)

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
print("\nIf responses are contextual with specific details (numbers, food names, etc.),")
print("then the chatbot is working correctly!")
