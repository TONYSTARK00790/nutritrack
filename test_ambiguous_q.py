"""
Final verification: Same ambiguous question, different reasons = different advice
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

user, _ = User.objects.get_or_create(username='ambig_test', defaults={'email': 'test@test.com'})
profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'goal': 'Gain Muscle'})

bot = SmartNutritionChatbot(user)

# THE SAME QUESTION asked from different "reason" contexts
ambiguous_q = "How can I gain weight?"

print("\n" + "="*80)
print("SAME QUESTION, DIFFERENT REASONS = DIFFERENT ADVICE")
print("="*80)
print(f"\nQuestion: '{ambiguous_q}'\n")

reasons = {
    'fitness': 'Training/Muscle focused',
    'nutrition': 'Diet/Calorie focused',
    None: 'No specific reason'
}

for reason, description in reasons.items():
    print(f"\n[Reason: {reason or 'NONE'} - {description}]")
    print("-" * 80)
    
    response = bot.get_response(ambiguous_q, reason=reason)
    
    # Extract first 3 lines
    lines = response.split('\n')[:3]
    preview = '\n'.join(lines)
    
    print(preview)
    print(f"\n Full response length: {len(response)} chars")

print("\n" + "="*80)
print("EXPECTED: Different reasons show different advice types")
print("  Fitness: Should mention training, progressive overload, lifts")
print("  Nutrition: Should mention calories, surplus, food, macros")
print("  None: Should auto-detect and show both perspectives")
print("="*80)
