from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import LikeViewSet, DislikeViewSet

router = DefaultRouter()
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'dislikes', DislikeViewSet, basename='dislike')

urlpatterns = [
    path('api/', include(router.urls)),

]
