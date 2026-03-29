from django.contrib import admin
from .models import UserProfile, ChatSession, ChatMessage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'weight', 'height', 'goal', 'calorie_goal']
    list_filter = ['gender', 'activity_level', 'goal']
    search_fields = ['user__username', 'user__email']


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['created_at']


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'reason', 'created_at']
    list_filter = ['reason', 'created_at']
    search_fields = ['user__username']
    inlines = [ChatMessageInline]
