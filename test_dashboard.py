#!/usr/bin/env python
import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

User = get_user_model()

# Create or get test user
user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})

client = Client()
client.force_login(user)

try:
    response = client.get('/dashboard/')
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"\nResponse Content (first 3000 chars):")
        content = response.content.decode('utf-8')
        print(content[:3000])
        # Look for error messages
        if 'error' in content.lower():
            print("\n[ERROR FOUND IN RESPONSE]")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
