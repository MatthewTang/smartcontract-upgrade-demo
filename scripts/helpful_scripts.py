from brownie import (
    network,
    accounts,
    config,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
)
import eth_utils

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development"]
LOCAL_BLOCK_CHAIN = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + ["mainnet-fork"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)

    if network.show_active() in LOCAL_BLOCK_CHAIN:
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


# initialiser=box.store, 1, 2, 3 etc
"""Encodes the func call so we can work with an initializer.
Args:
    initialiser ( [brownie.network.contract.ContractTx], optional):
    The initialiser func we want to call, Exaple: `box.store`.
    Defaults to None.

    args (any, optional):
    The arguments to pass to the initialiser func.

Returns:
    [bytes]: Return the encoded bytes
"""


def encode_function_data(initialiser=None, *args):
    if len(args) == 0 or not initialiser:
        return eth_utils.to_bytes(hexstr="0x")
    return initialiser.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initialiser=None,
    *args
):
    if proxy_admin_contract:
        if initialiser:
            encoded_function_call = encode_function_data(initialiser, *args)
            # proxyAdmin's upgradeAndCall(TransparentUpgradeableProxy proxy,address implementation, bytes memory data)
            tx = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            tx = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    else:
        if initialiser:
            encoded_function_call = encode_function_data(initialiser, *args)
            tx = proxy.upgradeToAndCall(
                new_implementation_address, encoded_function_call, {"from": account}
            )
        else:
            tx = proxy.upgradeTo(new_implementation_address, {"from": account})

    return tx


def deploy_box_v1_and_proxy():
    """Deploy boxV1, proxyAdmin and proxy
    Args:

    Returns:
        [brownie.network.contract.ProjectContract]box,
        [brownie.network.contract.ProjectContract]proxy_admin,
        [brownie.network.contract.ProjectContract]proxy,
        [brownie.network.contract.ProjectContract]proxy_box
    """
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initialiser_func = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initialiser_func,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    return box, proxy_admin, proxy, proxy_box
