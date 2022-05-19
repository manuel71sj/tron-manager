import logging

# Create your views here.
from django.http import JsonResponse
from rest_framework import viewsets, permissions

from framework.user.models import User
from framework.user.serializers import UserSerializer

logger = logging.getLogger(__name__)


def index(request):
    logger.debug("user = %s" % request.user)
    try:
        3 / 0
    except Exception as e:
        logger.exception(e)

    return JsonResponse({"result": True})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, args, kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(self, request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)
