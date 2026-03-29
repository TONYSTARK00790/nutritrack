from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'nt-input'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'nt-input'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'height', 'weight', 'activity_level', 'goal', 'training_style', 'calorie_goal']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'nt-input', 'placeholder': 'e.g. 25'}),
            'gender': forms.Select(attrs={'class': 'nt-input'}),
            'height': forms.NumberInput(attrs={'class': 'nt-input', 'placeholder': 'cm e.g. 170'}),
            'weight': forms.NumberInput(attrs={'class': 'nt-input', 'placeholder': 'kg e.g. 70'}),
            'activity_level': forms.Select(attrs={'class': 'nt-input'}),
            'goal': forms.Select(attrs={'class': 'nt-input'}),
            'training_style': forms.Select(attrs={'class': 'nt-input'}),
            'preferred_workout_type': forms.Select(attrs={'class': 'nt-input'}),
            'calorie_goal': forms.NumberInput(attrs={'class': 'nt-input', 'placeholder': 'e.g. 2000'}),
        }
