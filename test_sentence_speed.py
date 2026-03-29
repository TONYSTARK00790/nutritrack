import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.enhanced_chatbot import SmartNutritionChatbot

# Create test user if needed
user, created = User.objects.get_or_create(username='speedtest', defaults={'email': 'speedtest@test.com'})

# Initialize chatbot
chatbot = SmartNutritionChatbot(user)

# Test sentences
test_queries = [
    "lose weight",  
    "can i lose weight by doing cardio three times a week",  
    "i want to gain muscle should i eat more",  
    "what's the best workout for fat loss",  
    "how much protein do i need",  
]

print("=" * 60)
print("SENTENCE PROCESSING SPEED TEST")
print("=" * 60)

for query in test_queries:
    start = time.time()
    response = chatbot.get_response(query)
    elapsed = time.time() - start
    
    print("\nQuery: " + query)
    print("Time: " + str(elapsed*1000) + "ms")
    if response and len(response) > 80:
        print("Response: " + response[:80] + "...")
    else:
        print("Response: " + str(response))

print("\n" + "=" * 60)
print("OK - All tests completed!")
print("=" * 60)
