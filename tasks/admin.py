from django.contrib import admin
from .models import Task, Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'completed', 'due_date', 'created_at']
    list_filter = ['completed', 'group', 'created_at', 'due_date']
    search_fields = ['title', 'description']
    list_editable = ['completed']
