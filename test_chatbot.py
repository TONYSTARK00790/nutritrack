#!/usr/bin/env python
"""
Test script for the enhanced chatbot functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from accounts.enhanced_chatbot import SmartNutritionChatbot
from accounts.models import UserProfile
from django.contrib.auth.models import User

def test_chatbot():
    """Test the enhanced chatbot with various queries"""

    # Create a test user if needed
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user('testuser', 'test@example.com', 'password123')
        UserProfile.objects.create(user=user, preferred_workout_type='strength')

    # Initialize chatbot with user
    chatbot = SmartNutritionChatbot(user)

    # Test queries with appropriate reasons
    test_queries = [
        ("how much calories in biryani", "nutrition"),
        ("what's the protein in chicken breast", "nutrition"),
        ("I'm feeling sore after workout", "health"),
        ("I have low energy all the time", "health"),
        ("I'm stressed and anxious", "health"),
        ("I can't sleep well", "health"),
        ("how to recover from overtraining", "health"),
        ("joint pain in knees", "health"),
        ("gut health issues", "health"),
        ("mental focus problems", "health")
    ]

    print("🧪 Testing Enhanced Chatbot Responses\n")
    print("=" * 50)

    for query, reason in test_queries:
        print(f"\n❓ Query: '{query}' (reason: {reason})")
        print("-" * 40)

        # Get response (we'll use dummy data since we can't access real user data easily)
        dummy_data = {
            'nutrition': {
                'today': {'calories': 1800, 'protein': 120, 'carbs': 200, 'fat': 70, 'meals_count': 3},
                'goal': 2200,
                'remaining': 400,
                'progress': 82,
                'targets': {'protein': 150, 'carbs': 250, 'fat': 75}
            },
            'fitness': {
                'weekly': {'workouts': 4, 'total_volume': 12000},
                'streak': 12
            }
        }

        try:
            response = chatbot.get_response(query, reason=reason)
            print(f"🤖 Response: {response[:200]}..." if len(response) > 200 else f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")

        print()

if __name__ == '__main__':
    test_chatbot()