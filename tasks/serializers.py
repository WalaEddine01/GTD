from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Group


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'date_joined']
        read_only_fields = ['id', 'date_joined']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class GroupSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    task_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'created_at', 'owner', 'owner_username', 'task_count']
        read_only_fields = ['id', 'created_at', 'owner']
        
    def get_task_count(self, obj):
        return obj.task_set.count()


class TaskSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'completed', 
            'created_at', 'updated_at', 'group', 'group_name', 
            'owner', 'owner_username'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']
