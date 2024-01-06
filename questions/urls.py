from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/questions/user_questions/',
         QuestionViewSet.as_view({'get': 'user_questions'}), name='user-questions'),
    path('api/questions/topic_questions/<int:topic_id>/',
         QuestionViewSet.as_view({'get': 'topic_questions'}), name='topic-questions')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
