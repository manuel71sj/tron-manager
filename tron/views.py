# Create your views here.
import logging

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, renderer_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from tronpy import Tron
from tronpy.keys import PrivateKey

from boot.config import TRON
from boot.exceptions import BusinessError
from boot.renderers import CustomRenderer
from contract.models import Contract
from contract.serializers import ContractSerializer
from framework.module.common import is_url
from transaction.models import Transaction
from transaction.serializers import TransactionSerializer
from tron.module import compile_nft, get_contract
from tron.serializers import TronCreateSerializer, TronMintSerializer
from wallet.models import Wallet

logger = logging.getLogger(__name__)

tron = Tron(network=TRON['network'])


@swagger_auto_schema(method='post', request_body=TronCreateSerializer, )
@api_view(['POST'])
@renderer_classes([CustomRenderer])
@permission_classes([AllowAny])
def contract_create(request):
    serializer = TronCreateSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    try:

        wallet_id = request.session['w-k']
        wallet = Wallet.objects.get(id=wallet_id, user=request.user)

        priv_key = PrivateKey.fromhex(wallet.private_key)
        address = priv_key.public_key.to_base58check_address()

        if (wallet.address != address):
            raise BusinessError(_('PrivateKey address mismatch'))

        cntr = compile_nft(name=serializer.data['name'], symbol=serializer.data['symbol'])

        txn = (
            tron.trx.deploy_contract(priv_key.public_key.to_base58check_address(), cntr)
                .fee_limit(10 ** 9)
                .build()
                .sign(priv_key)
        )
        result = txn.broadcast().wait()

        '''
        result.get('result')) 가 success 일때만 계속 진행, failed여도 contract_address가 생성됨
        '''

        transaction = Transaction.crate_contract(txn.txid, result, request.user)
        contract = Contract.create_nft_contract(transaction, wallet, request.user,
                                                get_contract(transaction.contract_address),
                                                serializer.data['symbol'])

        return Response({
            'transaction': TransactionSerializer(transaction).data,
            'contract': ContractSerializer(contract).data,
        })
    except Exception as e:
        logger.exception(e)
        raise BusinessError(e)


@swagger_auto_schema(method='post', request_body=TronMintSerializer, )
@api_view(['post'])
@permission_classes([AllowAny])
def mint_nft(request):
    '''
    OWNER TV7XSJcaxxi8MA7ABqeDgY9uKSizCTZGkw
    35d80f0adb3149f594f32195603c2f27194c52d1da7e56046ce10b388f88a2ff
    1111111111111111111111111111111111111111111111111111111111111111
    0000000000000000000000000000000000000000000000000000000000000000
    MNT TR9tDQB1Q7YvXiM4TGEDH84uPzcoCD6qH8
    MNT3 TKa7pNb36iZ4zdE4o5G3C4qHPEKRsiRbEi
    MNT4 TDRq7N87Sa1hUfQpr1MjvSK4tWamnJSmmm
    MNT5 TGPgBNzTM2DzCyxV2i7k724qnt6E4LSX6n
    $(symbol)s TLdnQ7muoZmeC1nuoHvBeoZ1SQKszrNkAB
    MNT6 TR3DtmH9MdQ17XBFvVGQnKBu5LYJhdXHZM
    MNT7 TViALVCVs4vdPVXzQ7JSsQyZ3yPukJ4uzF

    TRANSFER TXL4JRFhiChH6X7Nn4C5zjh4DUSv6iPh3e
    '''
    try:
        serializer = TronMintSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        token_uri = serializer.data['token_uri']
        if (not is_url(token_uri)):
            raise BusinessError('token_uri(%s) is not uri type' % token_uri)

        token_id = serializer.data['token_id']
        if token_id == 0 or token_id == None:
            token_id = int(timezone.now().timestamp())

        wallet_id = request.session['w-k']
        wallet = Wallet.objects.get(id=wallet_id, user=request.user)

        private_key = PrivateKey.fromhex(wallet.private_key)
        address = private_key.public_key.to_base58check_address()

        if (wallet.address != address):
            raise BusinessError(_('PrivateKey address mismatch'))

        if address != serializer.data['owner_address']:
            raise BusinessError('owner_address(%s) is not match private key' % serializer.data[
                'owner_address'])

        contract = tron.get_contract(serializer.data['contract_address'])

        is_minter = contract.functions.isMinter(address)
        if (not is_minter):
            raise BusinessError(is_minter)

        to_address = serializer.data['to_address']
        if (not tron.is_address(to_address)):
            raise BusinessError('to_address(%s) is not address type' % to_address)

        mint = contract.functions.mintWithTokenURI(
            to_address,
            token_id,
            token_uri
        )

        trx = mint.with_owner(address).fee_limit(10 ** 9).build().sign(private_key)
        result = trx.broadcast().wait()

        # TODO : make celery job

        return Response({'contract': contract.name, 'symbol': contract.functions.symbol(), 'result': result})
    except Exception as e:
        logger.exception(e)
        raise BusinessError(e)


'''
컨펌된 블록 확인
getTransactionInfoById 로 blocknumber 확인 후
getNowBlock과의 차이를 카운트 하여 19 이상이면 confirm된 트랜젝션으로 확인

getTransactionById의 contractRet는 evm메세지 일뿐 최종 확인은 컨펌 수로 확인해야 함

대량 mint test
fee limit 150

'''


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)
