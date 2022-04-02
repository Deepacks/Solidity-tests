from brownie import FundMe

from scripts.helpers import get_account


def fund_fund():
    account = get_account()
    fund_contract = FundMe[-1]
    entrance_fee = fund_contract.getEntranceFee()
    # 14925373134328358

    transaction_receipt = fund_contract.fund(
        {"from": account, "amount": entrance_fee + 1}
    )
    transaction_receipt.wait(1)
    print(transaction_receipt)


def main():
    fund_fund()
