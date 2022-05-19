import logging
import math
from time import sleep

from bip32 import BIP32
from django.utils.translation import gettext_lazy as _
from mnemonic import Mnemonic
from tronpy import Tron
from tronpy.keys import PrivateKey

from boot.config import TRON

logger = logging.getLogger(__name__)

tron = Tron(network=TRON["network"])


def mnemonic_to_private_key(mnemonic: str) -> PrivateKey:
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic, passphrase="")
    node = BIP32.from_seed(seed)

    child = node.get_privkey_from_path("m/44'/195'/0'/0/0")
    return PrivateKey(child)


def private_key_to_address(private_key: PrivateKey) -> str:
    return private_key.public_key.to_base58check_address()


def mnemonic_to_address(mnemonic: str) -> str:
    return private_key_to_address(mnemonic_to_private_key(mnemonic))


def to_sun(amount: float) -> int:
    return int(amount * 1_000_000)


def from_sun(amount: int) -> float:
    return amount / 1_000_000


def get_bandwidth_status(address: str):
    resource = tron.get_account_resource(address)

    total = resource.get("freeNetLimit")
    used = resource.get("freeNetUsed")

    if used is None:
        used = 0

    percent = math.floor((used / total) * 100)

    logger.info(
        _("계정 %s 대역폭: 사용: %s, 최대: %s, 사용율: %s") % (address, used, total, percent)
    )
    return percent


def securing_bandwidth(address: str):
    while get_bandwidth_status(address) > 90:
        logger.info(_("계정 %s의 사용중인 대역폭이 90%를 초과 하였습니다. 20분간 대기 합니다.") % address)
        sleep(1 * 60 * 20)
