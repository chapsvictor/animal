from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRegistrationViewSet


router = DefaultRouter()
router.register('user', UserViewSet, basename='user_view')
router.register('user-registration', UserRegistrationViewSet, basename='user_register_view')

urlpatterns = [
    path('', include(router.urls)),
]
