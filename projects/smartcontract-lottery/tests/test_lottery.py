from brownie import Lottery, accounts, config, network
from web3 import Web3

# 0,014285714285714
# 14285714285714000


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )

    entrance_fee = lottery.getEntranceFee()
    print(entrance_fee)

    # assert entrance_fee > Web3.toWei(0.013, "ether")
    # assert entrance_fee < Web3.toWei(0.015, "ether")
