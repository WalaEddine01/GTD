from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='task_groups',
        null=True,  # Allow null temporarily for migration
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.owner.username if self.owner else 'No owner'})"

    class Meta:
        ordering = ['name']


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_tasks',
        null=True,  # Allow null temporarily for migration
        blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.owner.username if self.owner else 'No owner'})"

    class Meta:
        ordering = ['-created_at']
