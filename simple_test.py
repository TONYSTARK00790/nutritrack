#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from accounts.enhanced_chatbot import SmartNutritionChatbot
from accounts.models import UserProfile
from django.contrib.auth.models import User

# Get test user
user = User.objects.filter(username='test_user').first()
if not user:
    user = User.objects.create_user('test_user', 'test@example.com', 'password123')
    UserProfile.objects.create(user=user, age=25, gender='M', height=175, weight=70, goal='maintain', activity_level='moderate')

chatbot = SmartNutritionChatbot(user)

test_messages = [
    "How much protein do I need?",
    "How can I increase lean muscle?",
    "I'm feeling tired",
    "What's in chicken?",
    "Help me lose weight",
    "I ate too much today"
]

for msg in test_messages:
    response = chatbot.get_response(msg, reason='nutrition')
    print(f"Q: {msg}")
    print(f"A: {response}")
    print("-" * 50)