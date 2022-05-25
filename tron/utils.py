import itertools
import logging
import math
from time import sleep

from bip32 import BIP32
from django.utils.translation import gettext_lazy as _
from mnemonic import Mnemonic
from tronpy import Tron
from tronpy.keys import PrivateKey
from trx_utils import is_boolean, is_integer, to_hex, remove_0x_prefix, decode_hex
from trx_utils.encoding import int_to_big_endian

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


def has_one_val(*args, **kwargs):
    vals = itertools.chain(args, kwargs.values())
    not_nones = list(filter(lambda val: val is not None, vals))
    return len(not_nones) == 1


def assert_one_val(*args, **kwargs):
    if not has_one_val(*args, **kwargs):
        raise TypeError(
            "Exactly one of the passed values can be specified. "
            "Instead, values were: %r, %r" % (args, kwargs)
        )


def to_text(primitive=None, hexstr=None, text=None):
    assert_one_val(primitive, hexstr=hexstr, text=text)

    if hexstr is not None:
        return to_bytes(hexstr=hexstr).decode("utf-8")
    elif text is not None:
        return text
    elif isinstance(primitive, str):
        return to_text(hexstr=primitive)
    elif isinstance(primitive, bytes):
        return primitive.decode("utf-8")
    elif is_integer(primitive):
        byte_encoding = int_to_big_endian(primitive)
        return to_text(byte_encoding)
    raise TypeError("Expected an int, bytes or hexstr.")


def to_bytes(primitive=None, hexstr=None, text=None):
    assert_one_val(primitive, hexstr=hexstr, text=text)

    if is_boolean(primitive):
        return b"\x01" if primitive else b"\x00"
    elif isinstance(primitive, bytes):
        return primitive
    elif is_integer(primitive):
        return to_bytes(hexstr=to_hex(primitive))
    elif hexstr is not None:
        if len(hexstr) % 2:
            hexstr = "0x0" + remove_0x_prefix(hexstr)
        return decode_hex(hexstr)
    elif text is not None:
        return text.encode("utf-8")
    raise TypeError("expected an int in first arg, or keyword of hexstr or text")
