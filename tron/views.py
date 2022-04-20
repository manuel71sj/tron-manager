# Create your views here.
import logging

import eth_keys
import tronpy
from django.http import JsonResponse
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from solcx.exceptions import SolcError
from tronapi import Tron as TR, HttpProvider
from tronpy import Tron
from tronpy.exceptions import BadKey
from tronpy.keys import PrivateKey

from framework.module.common import is_url
from tron.module import compile_nft
from tron.serializers import TronCreateSerializer, TronMintSerializer

logger = logging.getLogger(__name__)

full_node = HttpProvider('https://api.shasta.trongrid.io')
solidity_node = HttpProvider('https://api.shasta.trongrid.io')
event_server = HttpProvider('https://api.shasta.trongrid.io')

tron = Tron(network='shasta')

tr = TR(full_node=full_node,
        solidity_node=solidity_node,
        event_server=event_server)


@swagger_auto_schema(method='post', request_body=TronCreateSerializer, )
@api_view(['POST'])
@permission_classes([AllowAny])
def contract_create_sample(request):
    tr.private_key = '35d80f0adb3149f594f32195603c2f27194c52d1da7e56046ce10b388f88a2ff'
    tr.default_address = tr.address.from_private_key(tr.private_key).base58  # 'TV7XSJcaxxi8MA7ABqeDgY9uKSizCTZGkw'

    serializer = TronCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return JsonResponse({'result': 'FAILED'})

    try:
        priv_key = PrivateKey.fromhex(tr.private_key)

        cntr = compile_nft(name=serializer.data['name'], symbol=serializer.data['symbol'])

        txn = (
            tron.trx.deploy_contract(tr.default_address.get('base58'), cntr)
                .fee_limit(10 ** 9)
                .build()
                .sign(priv_key)
        )
        result = txn.broadcast().wait()

        '''
        result.get('result')) 가 success 일때만 계속 진행, failed여도 contract_address가 생성됨
        '''

        created_cntr = tron.get_contract(result['contract_address'])

        report = {
            'result': result,
            'txid': txn.txid,
            'contract_address': created_cntr.contract_address,
        }

        return JsonResponse({'report': report})
    except SolcError as solc_error:
        logger.exception(solc_error)
        return JsonResponse({'result': 'FAILED', 'err': solc_error.message})
    except BadKey as bad_key:
        logger.exception(bad_key)
        return JsonResponse({'result': 'FAILED', 'err': bad_key.args})
    except TypeError as type_error:
        logger.exception(type_error)
        return JsonResponse({'result': 'FAILED', 'err': type_error.args})
    except eth_keys.exceptions.ValidationError as eth_keys_validation_error:
        logger.exception(eth_keys_validation_error)
        return JsonResponse({'result': 'FAILED', 'err': eth_keys_validation_error})
    except tronpy.exceptions.ValidationError as tronpy_validation_error:
        logger.exception(tronpy_validation_error)
        return JsonResponse({'result': 'FAILED', 'err': tronpy_validation_error.args})


@swagger_auto_schema(method='post', request_body=TronMintSerializer, )
@api_view(['post'])
@permission_classes([AllowAny])
def mint_nft_sample(request):
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

        if not serializer.is_valid():
            return JsonResponse({'result': 'FAILED', 'msg': 'validation failed'})

        token_uri = serializer.data['token_uri']
        if (not is_url(token_uri)):
            return JsonResponse({'result': 'FAILED', 'msg': 'token_uri(%s) is not uri type' % token_uri})

        token_id = serializer.data['token_id']
        if token_id == 0 or token_id == None:
            token_id = int(timezone.now().timestamp())

        tr.private_key = serializer.data['owner_private_key']
        tr.default_address = tr.address.from_private_key(tr.private_key).base58
        priv_key = PrivateKey.fromhex(tr.private_key)

        print(tr.private_key)
        print(tr.default_address)

        if tr.default_address.base58 != serializer.data['owner_address']:
            return JsonResponse({'result': 'FAILED',
                                 'msg': 'owner_address(%s) is not match private key' % serializer.data[
                                     'owner_address']})

        contract = tron.get_contract(serializer.data['contract_address'])

        is_minter = contract.functions.isMinter(tr.default_address.base58)
        if (not is_minter):
            return JsonResponse({'result': 'FAILED', 'msg': is_minter})

        to_address = serializer.data['to_address']
        if (not tron.is_address(to_address)):
            return JsonResponse({'result': 'FAILED', 'msg': 'to_address(%s) is not address type' % to_address})

        mint = contract.functions.mintWithTokenURI(
            to_address,
            token_id,
            token_uri
        )

        trx = mint.with_owner(tr.default_address.base58).fee_limit(10 ** 9).build().sign(priv_key)
        result = trx.broadcast().wait()

        return JsonResponse({'contract': contract.name, 'symbol': contract.functions.symbol(), 'result': result})
    except Exception as e:
        logger.exception(e)
        return JsonResponse({'result': 'FAILED', 'err': e.args})


def sample(request):
    # aa = '4174fcf179ef88f94a4ac2bfb7da0c9808573e11d9'
    bb = 'TKa7pNb36iZ4zdE4o5G3C4qHPEKRsiRbEi'
    return JsonResponse({'address': tron.address.to_hex(bb)})
