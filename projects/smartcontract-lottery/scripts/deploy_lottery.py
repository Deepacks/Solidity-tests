from brownie import accounts, config, network, Lottery


def deploy_lottery():
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["callback_gas_limit"],
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["s_subscriptionId"],
        {"from": accounts.add(config["wallets"]["from_key"])},
    )
    print("Contract deployed to {}".format(lottery.address))


def main():
    deploy_lottery()
