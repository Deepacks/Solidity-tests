from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts.add(config["wallets"]["from_key"])
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["callback_gas_limit"],
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["s_subscriptionId"],
        {"from": account},
    )

    print(lottery)

    entrance_fee = lottery.getEntranceFee()
    print(entrance_fee)

    assert entrance_fee > Web3.toWei(0.016, "ether")
    assert entrance_fee < Web3.toWei(0.017, "ether")
