import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
import django
django.setup()

from accounts.enhanced_chatbot import SmartNutritionChatbot
from django.contrib.auth.models import User

user = User.objects.first()
chat = SmartNutritionChatbot(user)

test_queries = [
    "what workouts should i do",
    "best workout routine for muscle gain",
    "how to start training",
    "workout plan",
    "i want to build muscle"
]

print("Testing workout queries:")
print("="*70)
for query in test_queries:
    response = chat.get_response(query, reason='fitness')
    print(f"Q: {query}")
    print(f"A: {response[:150]}..." if len(response) > 150 else f"A: {response}")
    print("-" * 70)
