#!/usr/bin/env python
import os
import sys
import django
import json
from django.test import Client
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

User = get_user_model()

# Create or get test user
user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})

client = Client()
client.force_login(user)

print("=" * 80)
print("TESTING CHATBOX ENDPOINTS")
print("=" * 80)

# Test 1: Create chat session
print("\n1. Testing create_chat_session endpoint...")
print("-" * 80)

response = client.post(
    '/accounts/api/chat/create/',
    data=json.dumps({'reason': 'fitness'}),
    content_type='application/json'
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json() if response.status_code == 200 else response.content.decode()[:500]}")

if response.status_code == 200:
    data = response.json()
    session_id = data.get('session_id')
    print(f"Session ID: {session_id}")
    
    # Test 2: Send message
    if session_id:
        print("\n2. Testing send_chat_message endpoint...")
        print("-" * 80)
        
        response = client.post(
            '/accounts/api/chat/send/',
            data=json.dumps({
                'session_id': session_id,
                'message': 'I am feeling tired and cannot work out'
            }),
            content_type='application/json'
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json() if response.status_code == 200 else response.content.decode()[:500]}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
