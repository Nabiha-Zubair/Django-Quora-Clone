from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FollowingViewSet

router = DefaultRouter()
router.register(r'followings', FollowingViewSet, basename='following')
urlpatterns = [
    path('api/', include(router.urls)),

]