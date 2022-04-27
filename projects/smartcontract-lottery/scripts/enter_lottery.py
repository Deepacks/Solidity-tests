from mmap import ACCESS_READ
from brownie import accounts, config, Lottery


def enter_lottery():
    contract = Lottery[-1]
    account = accounts.add(config["wallets"]["from_key"])


def main():
    enter_lottery()
