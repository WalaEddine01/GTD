from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, GroupViewSet, UserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'users', UserViewSet)
router.register(r'users/profile', UserViewSet, basename='user-profile')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),  # DRF login/logout views
]