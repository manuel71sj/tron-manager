from django.urls import path, include
from rest_framework.routers import DefaultRouter

from framework.user import views as user_views

app_name = "framework"

router = DefaultRouter()
router.register("users", user_views.UserViewSet, basename="users")

urlpatterns = [
    path("", user_views.index, name="user_index"),
    # path('users/', user_views.UserViewSet.as_view, name='user-list'),
    path("", include(router.urls)),
]
