"""
Test that chatbot provides relevant advice based on reason selected
Using actual topic-specific questions
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
user, _ = User.objects.get_or_create(username='reason_reply_test', defaults={'email': 'test@test.com'})
profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'goal': 'Gain Muscle'})

bot = SmartNutritionChatbot(user)

# More focused test cases
test_cases = [
    {
        "reason": "fitness",
        "question": "How do I build muscle?",
        "expected": ["strength", "progressive", "lift", "weight", "reps", "training"]
    },
    {
        "reason": "nutrition",
        "question": "How do I build muscle?",
        "expected": ["protein", "calorie", "surplus", "carbs", "food", "nutrition"]
    },
    {
        "reason": "health",
        "question": "How do I build muscle?",
        "expected": ["sleep", "recovery", "injury", "health", "wellnes", "rest"]
    },
    {
        "reason": "fitness",
        "question": "I feel tired",
        "expected": ["workout", "training", "exercise", "fitness"]
    },
    {
        "reason": "health",
        "question": "I feel tired",
        "expected": ["sleep", "energy", "hydration", "calories", "stress"]
    },
]

print("\n" + "="*80)
print("TESTING REASON-BASED RESPONSE CONTENT")
print("="*80 + "\n")

for i, test in enumerate(test_cases, 1):
    reason = test['reason']
    question = test['question']
    expected = test['expected']
    
    print(f"[Test {i}] Reason: {reason.upper()}, Question: '{question}'")
    
    response = bot.get_response(question, reason=reason)
    
    # Check for expected keywords
    found = [kw for kw in expected if kw.lower() in response.lower()]
    
    print(f"Response preview: {response[:120]}...")
    print(f"Expected keywords: {expected}")
    print(f"Found: {found if found else '[NONE FOUND]'}")
    
    if found:
        print(f"✅ GOOD - Found {len(found)}/{len(expected)} expected keywords")
    else:
        print(f"⚠️ WARNING - No expected keywords found")
    
    print("-" * 80 + "\n")

print("="*80)
print("If most tests show ✅, then reason-based prioritization is working!")
print("="*80)
