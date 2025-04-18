from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import UserList, CreateUserView, ChangePasswordView

urlpatterns = [
    # Authentication
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token-refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserList.as_view()),
    path("user-registration/", CreateUserView.as_view()),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
