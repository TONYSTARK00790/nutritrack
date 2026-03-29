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

print("=" * 80)
print("CHECKING DASHBOARD HTML FOR CHATBOX ELEMENTS")
print("=" * 80)

response = client.get('/dashboard/')
content = response.content.decode('utf-8')

checks = [
    ('notWellBtn', 'id="notWellBtn"', 'Not Feeling Well button'),
    ('reasonModal', 'id="reasonModal"', 'Reason selection modal'),
    ('chatboxPanel', 'id="chatboxPanel"', 'Chatbox panel'),
    ('chatMessagesPanel', 'id="chatMessagesPanel"', 'Chat messages area'),
    ('reasonOptions', 'const reasonOptions', 'Reason options array'),
    ('startChat', 'function startChat', 'Start chat function'),
    ('updateChatInputUI', 'function updateChatInputUI', 'Update chat UI function'),
    ('sendMessage', 'function sendMessage', 'Send message function'),
    ('create_chat_session URL', '/accounts/api/chat/create/', 'Create chat session URL'),
    ('send_chat_message URL', '/accounts/api/chat/send/', 'Send chat message URL'),
]

print("\nChecking for required elements and functions:")
print("-" * 80)

all_present = True
for name, pattern, description in checks:
    present = pattern in content
    status = "[OK]" if present else "[MISSING]"
    print(f"{status} {description:<50} ({name})")
    if not present:
        all_present = False

print("\n" + "=" * 80)
if all_present:
    print("SUCCESS: All chatbox elements are present!")
    print("\nThe chatbox should be working. If it's not:")
    print("1. Check browser console for JavaScript errors (F12 > Console)")
    print("2. Check if 'Not Feeling Well' button is clickable")
    print("3. Check if the reason modal appears when button is clicked")
    print("4. Check if selecting a reason opens the chat")
else:
    print("ERROR: Some chatbox elements are missing!")
    print("This would prevent the chatbox from working.")
print("=" * 80)
