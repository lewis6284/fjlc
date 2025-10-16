from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r'post',PostViewSet)
router.register(r'taken-posts', TakenPostViewSet, basename='takenpost')
router.register(r"archives", ArchiveViewSet, basename="archive")
urlpatterns = [
    path("", include(router.urls)),
]
