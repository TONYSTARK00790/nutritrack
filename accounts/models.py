from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('light', 'Light (exercise 1-3 days/week)'),
        ('moderate', 'Moderate (exercise 3-5 days/week)'),
        ('active', 'Active (hard exercise 6-7 days/week)'),
        ('very_active', 'Very Active (very hard exercise & physical job)'),
    ]
    GOAL_CHOICES = [
        ('lose', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain', 'Gain Muscle'),
    ]
    WORKOUT_TYPE_CHOICES = [
        ('balanced', 'Balanced Mix'),
        ('hypertrophy', 'Hypertrophy (muscle growth)'),
        ('strength', 'Strength-focused'),
        ('endurance', 'Endurance/Cardio'),
    ]
    TRAINING_STYLE_CHOICES = [
        ('jeff_nippard', 'Jeff Nippard - Science-Based Training'),
        ('arnold_golden', 'Arnold Golden Era - High Volume Bodybuilding'),
        ('ronnie_coleman', 'Ronnie Coleman - Hardcore High Volume'),
        ('mixed', 'Mixed - Variety of All Styles'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    height = models.FloatField(null=True, blank=True, help_text='Height in cm')
    weight = models.FloatField(null=True, blank=True, help_text='Weight in kg')
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='moderate')
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, default='maintain')
    preferred_workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPE_CHOICES, default='balanced', null=True, blank=True)
    training_style = models.CharField(max_length=30, choices=TRAINING_STYLE_CHOICES, default='mixed', null=True, blank=True)
    calorie_goal = models.IntegerField(null=True, blank=True)
    dark_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def calculate_bmr(self):
        if not all([self.age, self.height, self.weight]):
            return None
        if self.gender == 'M':
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161

    def calculate_tdee(self):
        bmr = self.calculate_bmr()
        if bmr is None:
            return None
        multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9,
        }
        return round(bmr * multipliers.get(self.activity_level, 1.55))

    def get_calorie_targets(self):
        tdee = self.calculate_tdee()
        if tdee is None:
            return None
        return {
            'maintenance': tdee,
            'fat_loss': tdee - 500,
            'muscle_gain': tdee + 500,
            'protein_g': round((tdee * 0.30) / 4),
            'carbs_g': round((tdee * 0.40) / 4),
            'fat_g': round((tdee * 0.30) / 9),
        }

    @property
    def bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 1)
        return None

    @property
    def bmi_category(self):
        bmi = self.bmi
        if bmi is None:
            return 'Unknown'
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        return 'Obese'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class ChatSession(models.Model):
    REASON_CHOICES = [
        ('nutrition', 'Nutrition & Diet'),
        ('fitness', 'Fitness & Workouts'),
        ('health', 'Health & Wellness'),
        ('relationship', 'Relationship Problem'),
        ('friendship', 'Friendship Issue'),
        ('parents', 'Family/Parents'),
        ('work', 'Work Stress'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_reason_display()}"


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.get_role_display()}: {self.message[:50]}"
