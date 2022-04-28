import logging
from time import sleep

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tronpy import Tron
from tronpy.exceptions import AddressNotFound

from boot.celery import app
from boot.config import TRON
from framework.module.choices import ConfirmedChoices, ResultChoices
from transaction.models import Transaction
from transaction.serializers import TransactionSerializer
from tron.utils import mnemonic_to_private_key, to_sun, private_key_to_address, securing_bandwidth
from wallet.models import Wallet

logger = logging.getLogger(__name__)

tron = Tron(network=TRON['network'])


@app.task
def check_transaction(tx_id: str):
    now = int(timezone.now().timestamp())

    transaction = Transaction.objects.filter(tx_id=tx_id).order_by('-updated_at')

    if len(transaction) <= 0:
        return False

    time_stamp = int(transaction[0].json_result['blockTimeStamp'] / 1000)

    while (time_stamp + 80) > now:
        ''' 트랜젝션이 발생한 시간 + 80초가 현재시간 보다 크면 10초 대기 후 재평가'''
        print('sleep 10s time_stamp: %s, now: %s' % (time_stamp, now))
        sleep(10)
        now = int(timezone.now().timestamp())

    tnx_info = tron.get_transaction_info(tx_id)
    latest_block_num = tron.get_latest_block_number()

    while (latest_block_num - tnx_info['blockNumber']) < 20:
        ''' 블럭수가 20개보다 작을 경우 10초 대기 후 재평가'''
        print('sleep 10s tnx: %s, latest: %s' % (tnx_info['blockNumber'], latest_block_num))
        sleep(10)
        latest_block_num = tron.get_latest_block_number()

    tnx = tron.get_transaction(tx_id)

    result = ResultChoices.PENDING
    confirmed = ConfirmedChoices.UNCONFIRMED

    if 'ret' in tnx:
        result = tnx['ret'][0]['contractRet']

    if (latest_block_num - tnx_info['blockNumber']) > 20:
        confirmed = ConfirmedChoices.CONFIRMED

    transaction[0].result = result
    transaction[0].status = confirmed

    transaction[0].save()


@app.task
def check_wallet_status():
    wallets = Wallet.objects.filter(active=False)

    if wallets.exists():
        for item in wallets.iterator():
            try:
                tron.get_account(item.address)

                item.active = True
                item.save()
                logger.info(_('%s (id: %s)는 활성화 되었습니다') % (item.address, item.id))
            except AddressNotFound:
                logger.info(_('%s (id: %s)는 비활성 상태입니다') % (item.address, item.id))


@app.task
def send_trx(from_address: str, to_address: str, amount: float, memo: str, mnemonic: str) -> object:
    private_key = mnemonic_to_private_key(mnemonic)

    securing_bandwidth(private_key_to_address(private_key))

    txn = (
        tron.trx.transfer(from_address, to_address, to_sun(amount))
            .memo(memo)
            .build()
            .sign(private_key)
    )

    result = txn.broadcast().wait()

    transaction = Transaction.create_send_transaction(txn.txid, result)

    check_transaction.delay(txn.txid)

    return {
        'tx_id': txn.txid,
        'result': result,
        'transaction': TransactionSerializer(transaction).data
    }
