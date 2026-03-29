from django import forms
from .models import CustomWorkoutRoutine, Workout


class CustomWorkoutRoutineForm(forms.ModelForm):
    """Form for creating/editing routine details (name & description only)"""
    
    class Meta:
        model = CustomWorkoutRoutine
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': 'e.g., Full Body Monday',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white resize-none',
                'rows': 3,
                'placeholder': 'Describe your routine strategy and goals...'
            }),
        }
        labels = {
            'name': 'Routine Name',
            'description': 'Description (Optional)',
        }


class AddWorkoutToRoutineForm(forms.Form):
    """Form for adding a single workout to a routine"""
    
    workout = forms.ModelChoiceField(
        queryset=Workout.objects.all().order_by('workout_type', 'name'),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white',
        }),
        label='Select Workout to Add'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize dropdown to show workout details
        self.fields['workout'].queryset = Workout.objects.all().order_by('workout_type', 'name')

