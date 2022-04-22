import logging
from typing import Optional

import solcx
from django.template.loader import render_to_string
from tronpy import Contract, Tron

from boot.settings import STATIC_ROOT
from wallet.models import Wallet

logger = logging.getLogger(__name__)


def compile_nft(name: str, symbol: str) -> Contract:
    """
    solidity TRC721 코드를 기반으로 컴파일 된 바이너리를 생성한다


    Args:
        name (str):  토큰이름
        symbol (str):  토큰심볼

    Returns:
        Contract (Contract):  컴파일된 바이너리 코드
    """
    solcx.install.get_executable('0.5.18', STATIC_ROOT / 'solcd/')

    context = dict(name=name, symbol=symbol)
    sol = render_to_string('contract/nft.sol', context)

    compiled_sol = solcx.compile_source(
        sol,
        output_values=['abi', 'bin'],
    )

    contract_interface = compiled_sol['<stdin>:TRC721Token']

    return Contract(name=name, bytecode=contract_interface['bin'], abi=contract_interface['abi'])


def generate_wallet(passphrase: str = None) -> dict:
    """
    지갑을 생성한다.

    Args:
        passphrase : 비밀번호 문구

    Returns:
        dict : {
            "base58check_address": priv_key.public_key.to_base58check_address(),
            "hex_address": priv_key.public_key.to_hex_address(),
            "private_key": priv_key.hex(),
            "public_key": priv_key.public_key.hex(),
        }

    """
    tron = Tron(network='shasta')

    if passphrase:
        address = tron.get_address_from_passphrase(passphrase)
    else:
        address = tron.generate_address()

    address['passphrase'] = passphrase
    return address


def get_match_user_and_address(address: str, user_id: int) -> Optional[str]:
    wallet = Wallet.objects.filter(user_id=user_id, address=address)
    if wallet.count() > 0:
        return wallet[0].private_key
    else:
        return None


def get_band_width(address: str):
    tron = Tron(network='shasta')

    pass
