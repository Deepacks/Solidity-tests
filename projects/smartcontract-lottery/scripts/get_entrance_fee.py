from brownie import Lottery


def get_entrance_fee():
    contract = Lottery[-1]
    entrance_fee = contract.getEntranceFee()

    print("The current entrance fee is {} wei".format(entrance_fee))


def main():
    get_entrance_fee()
