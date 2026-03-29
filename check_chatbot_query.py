import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from accounts.enhanced_chatbot import SmartNutritionChatbot
from django.contrib.auth.models import User
from accounts.models import UserProfile

user, _ = User.objects.get_or_create(username='test_user', defaults={'email': 'test@example.com'})
if not hasattr(user, 'profile'):
    UserProfile.objects.create(user=user, age=28, gender='M', height=180, weight=75, activity_level='moderate', goal='lose')

chat = SmartNutritionChatbot(user)
print(chat.get_response('how can i increase lean muscle', reason='fitness'))
print(chat.get_response('I ate too much today', reason='nutrition'))
print(chat.get_response('what should I eat for dinner', reason='nutrition'))

