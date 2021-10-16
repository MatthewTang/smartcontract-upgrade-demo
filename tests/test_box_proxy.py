from scripts.helpful_scripts import encode_function_data, get_account
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract
import pytest


def test_proxy_delegates_calls():
    # arrange
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
    # assert
    assert proxy_box.retrieve() == 0
    # act
    proxy_box.store(1, {"from": account}).wait(1)
    # assert
    assert proxy_box.retrieve() == 1


def test_proxy_box1_cant_increment():
    # arrange
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
    # act
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    with pytest.raises(AttributeError):
        proxy_box.increment({"from": account})
