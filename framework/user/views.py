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

    return JsonResponse({'result': True})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
