from brownie import (
    network,
    accounts,
    config,
)

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
