"""
Verify that the chatbox appears on the dashboard template
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Create test user if doesn't exist
user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})

# Make request to dashboard
client = Client()
client.force_login(user)
response = client.get('/dashboard/')

print("\n" + "="*80)
print("CHECKING CHATBOX VISIBILITY")
print("="*80)

# Check if key elements are in the response
checks = [
    ('chatboxPanel', 'id="chatboxPanel"' in response.content.decode()),
    ('Start Chat button', 'Start Chat' in response.content.decode()),
    ('Chat input field', 'chatInputField' in response.content.decode()),
    ('Reason modal', 'id="reasonModal"' in response.content.decode()),
    ('Send button', 'id="sendBtn"' in response.content.decode()),
    ('Chat messages panel', 'id="chatMessagesPanel"' in response.content.decode()),
]

print("\nTemplate Elements Found:")
print("-" * 80)
all_good = True
for name, found in checks:
    status = "[OK]" if found else "[MISSING]"
    print(f"{status} {name}")
    if not found:
        all_good = False

print("\n" + "="*80)
if all_good:
    print("[OK] ALL CHATBOX ELEMENTS ARE PRESENT")
    print("\nNEXT STEPS:")
    print("1. Reload the dashboard page: http://localhost:8000/accounts/dashboard/")
    print("2. Look for the BLUE 'Start Chat' button in the right sidebar")
    print("3. Click it to open the chat reason selector")
    print("4. Choose a reason (Fitness, Nutrition, Health, etc.)")
    print("5. Type your question in the input field")
    print("6. Hit Send!")
else:
    print("[ERROR] Some chatbox elements are missing!")
    print("Check the template for syntax errors")

print("="*80)
