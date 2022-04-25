# Create your views here.
import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from tron.module import generate_wallet
from wallet.models import Wallet
from wallet.serializers import WalletSerializer, WalletCreateSerializer

logger = logging.getLogger(__name__)


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all().order_by('-created_at')
    serializer_class = WalletSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user, deleted=False).order_by('-created_at')

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


@swagger_auto_schema(method='post', request_body=WalletCreateSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_wallet(request):
    """
    지갑 생성

    Args:
        request: { passphrase: '암호' or None }
    """
    serializer = WalletCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return JsonResponse({'result': 'FAILED', 'msg': 'validation failed'})

    result = generate_wallet(serializer.data['passphrase'])

    wallet = Wallet.objects.create(
        user=request.user,
        address=result['base58check_address'],
        private_key=result['private_key'],
        passphrase=result['passphrase']
    )

    return JsonResponse({'result': 'SUCCESS', 'data': {
        'wallet_id': wallet.id,
        'address': result['base58check_address'],
        'private_key': result['private_key'],
        'passphrase': result['passphrase']
    }})


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def use_wallet(request, pk):
    """
    사용할 지갑을 선택한다

    Args:
        request:
        pk: wallet_id

    Returns:
        null: 'SUCCESS' or 'FAILED'

    """
    wallet = Wallet.objects.filter(user=request.user, id=pk)

    if wallet.count() <= 0:
        try:
            del request.session['w-k']
        except KeyError:
            pass

        return JsonResponse({'result': 'FAILED'})

    request.session['w-k'] = wallet[0].id
    return JsonResponse({
        'result': 'SUCCESS'
    })


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_session(request):
    print(request.session.__dict__)

    APIException

    try:
        return JsonResponse({
            'result': 'SUCCESS',
            'data': request.session['w-k']
        })
    except KeyError:
        return JsonResponse({
            'result': 'SUCCESS',
            'data': None
        })
