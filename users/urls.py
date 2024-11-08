from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users import views

router = DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('verify/', views.VerifyView.as_view()),
    path('verify/resend/', views.ResendVerifyView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('me/', views.UserProfile.as_view()),
    path('', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
