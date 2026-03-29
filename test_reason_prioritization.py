"""
Test that chatbot prioritizes responses based on the reason selected
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
user, _ = User.objects.get_or_create(username='reason_test', defaults={'email': 'test@test.com'})
profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'goal': 'Gain Muscle'})

# Initialize bot
bot = SmartNutritionChatbot(user)

# Same question, different reasons
question = "What should I focus on?"

reasons = ['fitness', 'nutrition', 'health', 'motivation', None]

print("\n" + "="*80)
print("TESTING REASON-BASED RESPONSE PRIORITIZATION")
print("="*80)

print(f"\n** Question (same for all): '{question}' **\n")

for reason in reasons:
    print(f"\n[Reason: {reason or 'NONE'}]")
    print("-" * 80)
    
    response = bot.get_response(question, reason=reason)
    
    # Show first 150 chars
    preview = response[:200] + "..." if len(response) > 200 else response
    print(f"Response: {preview}")
    
    # Detect what topic was prioritized
    if 'fitness' in response.lower() or 'workout' in response.lower() or 'training' in response.lower():
        print("  -> PRIORITIZED: Fitness")
    if 'nutrition' in response.lower() or 'protein' in response.lower() or 'calorie' in response.lower():
        print("  -> PRIORITIZED: Nutrition")
    if 'health' in response.lower() or 'sleep' in response.lower() or 'recovery' in response.lower():
        print("  -> PRIORITIZED: Health")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
print("\nExpected: Each reason prioritizes its corresponding topic")
print("eg: reason='fitness' should show fitness-focused advice")
print("    reason='nutrition' should show nutrition-focused advice")
print("    reason='health' should show health-focused advice")
