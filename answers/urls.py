from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import AnswerViewSet

router = DefaultRouter()
router.register(r'answers', AnswerViewSet, basename='answer')
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/answers/user_answers/',
         AnswerViewSet.as_view({'get': 'user_answers'}), name='user-answers'),
    path('api/answers/question_answers/<int:q_id>/',
         AnswerViewSet.as_view({'get': 'question_answers'}), name='question_answers'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
