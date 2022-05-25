# Create your views here.
import logging

from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import (
    api_view,
    renderer_classes,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tronpy import Tron

from boot.config import TRON
from boot.exceptions import BusinessError
from boot.renderers import CustomRenderer
from transaction import tasks
from transaction.models import Transaction
from transaction.serializers import (
    SendTrxSerializer,
    GetTrxResultByTxId,
    TransactionSerializer,
)
from tron.utils import to_text
from wallet.models import Wallet

logger = logging.getLogger(__name__)


@csrf_exempt
@swagger_auto_schema(method="post", request_body=SendTrxSerializer)
@api_view(["post"])
@renderer_classes([CustomRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def send_tron(request):
    serializer = SendTrxSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:

        # 보유한 address 인지 확인
        wallet = Wallet.objects.get(
            address=serializer.data["from_address"], user=request.user
        )

        result = tasks.send_trx_with_private_key.delay(
            wallet.address,
            serializer.data["to_address"],
            serializer.data["amount"],
            serializer.data.get("message", None),
            wallet.private_key,
            user_id=request.user.id,
            url=serializer.data.get("callback_url", None),
        )

        while not result.ready():
            pass

        return Response({"result": result.get()})

    except Exception as e:
        logger.exception(e)
        raise BusinessError(e)


@csrf_exempt
@swagger_auto_schema(method="post", request_body=GetTrxResultByTxId)
@api_view(["post"])
@renderer_classes([CustomRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_trx_result(request):
    serializer = GetTrxResultByTxId(data=request.data)
    serializer.is_valid()

    try:
        return Response(
            {
                "result": TransactionSerializer(
                    Transaction.objects.get(tx_id=serializer.data["tx_id"])
                ).data
            }
        )
    except Exception as e:
        logger.exception(e)
        raise BusinessError(e)


@csrf_exempt
@swagger_auto_schema(method="post", request_body=GetTrxResultByTxId)
@api_view(["post"])
@renderer_classes([CustomRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_trx_by_hash(request):
    serializer = GetTrxResultByTxId(data=request.data)
    serializer.is_valid()

    try:
        return Response(
            {
                "result": TransactionSerializer(
                    Transaction.objects.get(tx_id=serializer.data["tx_id"])
                ).data
            }
        )
    except Exception as e:
        logger.exception(e)
        raise BusinessError(e)


@csrf_exempt
@swagger_auto_schema(method="post", request_body=GetTrxResultByTxId)
@api_view(["post"])
@renderer_classes([CustomRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_message_by_hash(request):
    serializer = GetTrxResultByTxId(data=request.data)
    serializer.is_valid()

    try:
        tron = Tron(network=TRON["network"])
        tnx = tron.get_transaction(
            Transaction.objects.get(tx_id=serializer.data["tx_id"]).tx_id
        )

        return Response({"result": to_text(hexstr=tnx.get("raw_data").get("data"))})
    except Exception as e:
        logger.exception(e)
        raise BusinessError(e)
