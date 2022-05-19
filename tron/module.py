import logging
from typing import Optional

import solcx
from bip32 import BIP32
from django.template.loader import render_to_string
from mnemonic import Mnemonic
from tronpy import Contract, Tron
from tronpy.exceptions import AddressNotFound
from tronpy.keys import PrivateKey

from boot.config import TRON
from boot.settings import STATIC_ROOT
from transaction.tasks import send_trx
from tron.enums import TemplateMsg
from tron.utils import mnemonic_to_private_key, private_key_to_address
from wallet.models import Wallet

logger = logging.getLogger(__name__)

tron = Tron(network=TRON["network"])


def compile_nft(name: str, symbol: str) -> Contract:
    """
    solidity TRC721 코드를 기반으로 컴파일 된 바이너리를 생성한다


    Args:
        name (str):  토큰이름
        symbol (str):  토큰심볼

    Returns:
        Contract (Contract):  컴파일된 바이너리 코드
    """
    solcx.install.get_executable("0.5.18", STATIC_ROOT / "solcd/")

    context = dict(name=name, symbol=symbol)
    sol = render_to_string("contract/nft.sol", context)

    compiled_sol = solcx.compile_source(
        sol,
        output_values=["abi", "bin"],
    )

    contract_interface = compiled_sol["<stdin>:TRC721Token"]

    return Contract(
        name=name, bytecode=contract_interface["bin"], abi=contract_interface["abi"]
    )


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
    if passphrase:
        address = tron.get_address_from_passphrase(passphrase)
    else:
        address = tron.generate_address()

    address["passphrase"] = passphrase
    return address


def generate_address_with_passphrase() -> dict:
    """계정 생성"""
    while True:
        mnemo = Mnemonic("english")
        words = mnemo.generate(strength=128)
        seed = mnemo.to_seed(words, passphrase="")
        node = BIP32.from_seed(seed)

        child = node.get_privkey_from_path("m/44'/195'/0'/0/0")
        priv = PrivateKey(child)

        address = priv.public_key.to_base58check_address()

        try:
            tron.get_account(address)
        except AddressNotFound:
            result = {
                "passphrase": words,
                "address": address,
                "private_key": priv.hex(),
                "public_key": priv.public_key.hex(),
            }
            break

    """ 계정 초기화 """
    private_key = mnemonic_to_private_key(TRON["admin_mnemonic"])
    from_address = private_key_to_address(private_key)

    """
    wallet/createaccount
    을 호출하여 얻는 transactionref를 broadcast하여 계정 활성화 필요
    트론 그리드 접속 필요
    """

    send_trx.delay(
        from_address,
        result["address"],
        0.000001,
        TemplateMsg.ACCOUNT_INIT.get_value(),
        TRON["admin_mnemonic"],
    )

    return result


def get_match_user_and_address(address: str, user_id: int) -> Optional[str]:
    wallet = Wallet.objects.filter(user_id=user_id, address=address)
    if wallet.count() > 0:
        return wallet[0].private_key
    else:
        return None


def get_contract(contract_address: str) -> Contract:
    return tron.get_contract(contract_address)


# def send_trx(from_address: str, to_address: str, amount: float, memo: str, mnemonic: str) -> object:
#     private_key = mnemonic_to_private_key(mnemonic)
#
#     txn = (
#         tron.trx.transfer(from_address, to_address, to_sun(amount))
#             .memo(memo)
#             .build()
#             .sign(private_key)
#     )
#
#     result = txn.broadcast().wait()
#
#     transaction = Transaction.create_send_transaction(txn.txid, result)
#
#     tasks.check_transaction.delay(txn.txid)
#
#     return {
#         'tx_id': txn.txid,
#         'result': result,
#         'transaction': TransactionSerializer(transaction).data
#     }
