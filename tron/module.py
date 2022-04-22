import logging

import solcx
from django.template.loader import render_to_string
from tronpy import Contract, Tron

from boot.settings import STATIC_ROOT

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


def generate_wallet(passphrase) -> dict:
    tron = Tron(network='shasta')

    if passphrase:
        address = tron.get_address_from_passphrase(passphrase)
    else:
        address = tron.generate_address()

    address['passphrase'] = passphrase
    return address
