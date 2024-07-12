# tasks/models.py
from django.db import models

class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('work', 'Work'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    reminder_time = models.DateTimeField(blank=True, null=True)
    is_reminder_set = models.BooleanField(default=False)
    task_type = models.CharField(max_length=10, choices=TASK_TYPE_CHOICES, default='personal')

    def __str__(self):
        return self.title
