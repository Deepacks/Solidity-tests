from brownie import accounts, config, network, SimpleStorage


def deploy_simple_storage():
    account = get_account()

    simple_storage = SimpleStorage.deploy({"from": account})

    print("value", simple_storage.retrieve())
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    print("value", simple_storage.retrieve())


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
