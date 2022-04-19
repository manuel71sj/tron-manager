import solcx
from django.template.loader import render_to_string
from tronpy import Contract

from boot.settings import STATIC_ROOT


def compile_nft(name: str, symbol: str):
    solcx.install.get_executable('0.5.18', STATIC_ROOT / 'solcd/')

    context = dict(name=name, symbol=symbol)
    sol = render_to_string('contract/nft.sol', context)

    compiled_sol = solcx.compile_source(
        sol,
        output_values=['abi', 'bin'],
    )

    contract_interface = compiled_sol['<stdin>:TRC721Token']

    return Contract(name=name, bytecode=contract_interface['bin'], abi=contract_interface['abi'])
