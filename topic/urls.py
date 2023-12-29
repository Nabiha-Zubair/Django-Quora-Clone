from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import TopicViewSet

router = DefaultRouter()
router.register(r'topics', TopicViewSet, basename='topic')
urlpatterns = [
    path('api/', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
