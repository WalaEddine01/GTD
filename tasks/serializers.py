from rest_framework import serializers
from .models import Task, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'completed', 
            'created_at', 'updated_at', 'group', 'group_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
