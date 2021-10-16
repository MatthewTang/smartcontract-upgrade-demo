from scripts.helpful_scripts import get_account, upgrade, deploy_box_v1_and_proxy
from brownie import (
    BoxV2,
    Contract,
    exceptions,
)
import pytest


def test_proxy_upgrades():
    # arrange
    account = get_account()

    _, proxy_admin, proxy, _ = deploy_box_v1_and_proxy()

    # act
    box_v2 = BoxV2.deploy({"from": account})

    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})

    upgrade(account, proxy, box_v2.address, proxy_admin)
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from": account}).wait(1)
    assert proxy_box.retrieve() == 1
