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

    def get_permissions(self):
        """
        Allow user creation (registration) and listing without authentication for testing,
        but require authentication for other operations.
        """
        if self.action in ['create']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        - Superuser: Can see all users
        - Regular users: Can see all users (as per your requirement)
        - Unauthenticated: No access
        """
        if not self.request.user.is_authenticated:
            return User.objects.none()
        
        return User.objects.all().order_by('id')

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Groups with full CRUD operations.
    Users can only see and manage their own groups.
    """
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        - Superuser: Can see all groups
        - Regular users: Can see all groups (as per your requirement)
        - Unauthenticated: No access (handled by permission_classes)
        """
        if self.request.user.is_superuser:
            return Group.objects.all()
        else:
            return Group.objects.all()

    def perform_create(self, serializer):
        """Set the owner to the current user when creating a group"""
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        - Superuser: Can perform all operations on all groups
        - Regular users: Can view all groups, but only create/update/delete their own
        """
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        """Only allow users to update their own groups (unless superuser)"""
        group = self.get_object()
        if not request.user.is_superuser and group.owner != request.user:
            return Response(
                {"detail": "You can only update your own groups."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Only allow users to delete their own groups (unless superuser)"""
        group = self.get_object()
        if not request.user.is_superuser and group.owner != request.user:
            return Response(
                {"detail": "You can only delete your own groups."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """Get all tasks for a specific group"""
        group = self.get_object()
        
        if request.user.is_superuser:
            # Superuser can see all tasks in any group
            tasks = Task.objects.filter(group=group)
        else:
            # Regular users can only see their own tasks in the group
            tasks = Task.objects.filter(group=group, owner=request.user)
        
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Tasks with full CRUD operations.
    Users can only see and manage their own tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        - Superuser: Can see all tasks
        - Regular users: Can see only their own tasks
        - Unauthenticated: No access (handled by permission_classes)
        """
        if self.request.user.is_superuser:
            return Task.objects.all()
        else:
            # Regular users can only see their own tasks
            return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Set the owner to the current user when creating a task"""
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        """Only allow users to update their own tasks (unless superuser)"""
        task = self.get_object()
        if not request.user.is_superuser and task.owner != request.user:
            return Response(
                {"detail": "You can only update your own tasks."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Only allow users to delete their own tasks (unless superuser)"""
        task = self.get_object()
        if not request.user.is_superuser and task.owner != request.user:
            return Response(
                {"detail": "You can only delete your own tasks."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def toggle_completed(self, request, pk=None):
        """Toggle the completed status of a task"""
        task = self.get_object()
        if not request.user.is_superuser and task.owner != request.user:
            return Response(
                {"detail": "You can only toggle your own tasks."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
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
