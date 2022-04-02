from brownie import accounts, config, network, MockV3Aggregator

DECIMALS = 8
STARTING_PRICE = 335000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_price_feed_address(account):
    print("The active network is {}".format(network.show_active()))
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("Deploying mocks...")
        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": account})
            print("Mocks deployed!")
        else:
            print("Skipping mocks - already existing!")
        return MockV3Aggregator[-1].address
    else:
        return config["networks"][network.show_active()]["eth_usd_price_feed"]


def get_publish_source():
    return config["networks"][network.show_active()]["verify"]
