from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

urlpatterns = [
    path("", get_routes, name="routes"),
    path("projects", get_projects, name="get-projects"),
    path("projects/<uuid:pk>", get_project, name="get-project"),
    path("projects/<uuid:pk>/vote", vote_project, name="vote-project"),
    
    path("users/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
