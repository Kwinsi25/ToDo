# tasks/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    TASK_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('work', 'Work'),
    ]

    task_type = forms.ChoiceField(choices=TASK_TYPE_CHOICES, widget=forms.RadioSelect, initial='work')

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'reminder_time', 'is_reminder_set','task_type']
        widgets = {
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
