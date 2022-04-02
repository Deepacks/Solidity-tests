from brownie import FundMe

from scripts.helpers import get_account


def fund_withdraw():
    account = get_account()
    fund_contract = FundMe[-1]
    transaction_receipt = fund_contract.withdraw({"from": account})
    transaction_receipt.wait(1)
    print(transaction_receipt)


def main():
    fund_withdraw()
