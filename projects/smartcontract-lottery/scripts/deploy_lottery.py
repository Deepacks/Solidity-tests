from brownie import config, network, Lottery
from scripts.helpers import get_account, get_contract


def deploy_lottery():
    account = get_account(index=1)
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        config["networks"][network.show_active()]["callback_gas_limit"],
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["s_subscriptionId"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Contract deployed to {}".format(lottery.address))


def main():
    deploy_lottery()
