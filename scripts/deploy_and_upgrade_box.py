from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy(
        {"from": account}, publish_source=True
    )  # Box is our implementation contract ie it's implemented

    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)

    # encode the initialiser function, in bytes for _data param of TransparentUpgradableProxy
    # initialiser = box.store, 1
    # box_encoded_initialiser_function = encode_function_data(box.store, 1)
    box_encoded_initialiser_function = encode_function_data()
    # TransparentUgradeableProxy constructor( address logic, address admin, bytes data)
    # gas limit is put in as well, since sometimes proxies have a hard time figuring out the gas limit
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initialiser_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=True,
    )

    print(f"proxy deployed to {proxy}, you can now upgrade to v2!")
    # get contract using abi and address
    proxy_box = Contract.from_abi(
        "Box", proxy.address, Box.abi
    )  # since proxy delegate all calls to box
    print(proxy_box.retrieve())
    proxy_box.store(1, {"from": account}).wait(1)

    print(proxy_box.retrieve())

    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)

    # proxy_box.increment({"from": account}) -> 'Box' object has no attr 'increment'
    upgrade(account, proxy, box_v2.address, proxy_admin).wait(1)
    print("proxy has been upgraded!")

    proxy_box = Contract.from_abi(
        "BoxV2", proxy.address, BoxV2.abi
    )  # since proxy delegate all calls to box
    proxy_box.increment({"from": account}).wait(1)

    print(proxy_box.retrieve())
