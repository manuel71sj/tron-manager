# Create your views here.
import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from boot.exceptions import BusinessError
from boot.renderers import CustomRenderer
from tron.module import generate_wallet, generate_address_with_passphrase
from wallet.models import Wallet
from wallet.serializers import WalletSerializer, WalletCreateSerializer

logger = logging.getLogger(__name__)


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all().order_by('-created_at')
    serializer_class = WalletSerializer
    renderer_classes = [CustomRenderer]

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user, deleted=False).order_by('-created_at')

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


@swagger_auto_schema(method='post', request_body=WalletCreateSerializer, deprecated=True)
@api_view(['POST'])
@renderer_classes([CustomRenderer])
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
@renderer_classes([CustomRenderer])
@permission_classes([IsAuthenticated])
def create_wallet_with_passphrase(request):
    """
    암호로 지갑 생성
    """

    result = generate_address_with_passphrase()

    wallet = Wallet.objects.create(
        user=request.user,
        address=result['address'],
        private_key=result['private_key'],
        passphrase=result['passphrase']
    )

    result['wallet_id'] = wallet.id

    return Response(result)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@renderer_classes([CustomRenderer])
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

        raise BusinessError('FAILED')

    request.session['w-k'] = wallet[0].id
    return Response({
        'key_id ': wallet[0].id
    })


@swagger_auto_schema(method='get')
@api_view(['GET'])
@renderer_classes([CustomRenderer])
@permission_classes([IsAuthenticated])
def test_session(request):
    print(request.session.__dict__)

    try:
        return Response(request.session['w-k'])
    except Exception as e:
        logger.exception(e)
        raise BusinessError(e)

#  1,000,000,000
