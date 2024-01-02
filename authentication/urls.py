from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import signupView, loginView, logoutView, activate_user, get_csrf_token
from authentication.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path('csrf/', get_csrf_token),
    path('signup/', signupView, name='signup'),
    path('login/',  loginView, name='login'),
    path('logout/', logoutView, name='logout'),

    path('activate-user/<uidb64>/<token>',
         activate_user, name='activate'),
    path('api/', include(router.urls)),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
