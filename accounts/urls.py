from django.urls import path
from .views import RegisterApiView, CustomTokenObtainPairView, GetAllUsers
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_all_users/', GetAllUsers.as_view(), ),
]
