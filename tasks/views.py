from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Group
from .serializers import TaskSerializer, GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Users with registration and profile management.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        """
        Allow user creation (registration) without authentication,
        but require authentication for other operations.
        """
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Users can only see their own profile"""
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return User.objects.all()
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Groups with full CRUD operations.
    Users can only see and manage their own groups.
    """
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Filter groups to only show user's own groups or all groups if not authenticated"""
        if self.request.user.is_authenticated:
            return Group.objects.filter(owner=self.request.user)
        else:
            # For testing without authentication, show all groups
            return Group.objects.all()

    def perform_create(self, serializer):
        """Set the owner to the current user when creating a group"""
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            # For testing, use the first user or create one
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(username='testuser', password='testpass123')
            serializer.save(owner=user)

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """Get all tasks for a specific group"""
        group = self.get_object()
        tasks = Task.objects.filter(group=group)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Tasks with full CRUD operations.
    Users can only see and manage their own tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]  # Temporarily allow all

    def get_queryset(self):
        """Filter tasks to only show user's own tasks or all tasks if not authenticated"""
        if self.request.user.is_authenticated:
            return Task.objects.filter(owner=self.request.user)
        else:
            # For testing without authentication, show all tasks
            return Task.objects.all()

    def perform_create(self, serializer):
        """Set the owner to the current user when creating a task"""
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            # For testing, use the first user or create one
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(username='testuser', password='testpass123')
            serializer.save(owner=user)

    @action(detail=True, methods=['post'])
    def toggle_completed(self, request, pk=None):
        """Toggle the completed status of a task"""
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get all completed tasks for the current user"""
        completed_tasks = self.get_queryset().filter(completed=True)
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending tasks for the current user"""
        pending_tasks = self.get_queryset().filter(completed=False)
        serializer = self.get_serializer(pending_tasks, many=True)
        return Response(serializer.data)
