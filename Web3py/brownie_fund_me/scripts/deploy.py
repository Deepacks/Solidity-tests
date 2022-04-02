from brownie import FundMe

from scripts.helpers import get_account, get_price_feed_address, get_publish_source


def deploy_fund_me():
    account = get_account()
    feed_address = get_price_feed_address(account)
    publish_source = get_publish_source()

    fund_me = FundMe.deploy(
        feed_address, {"from": account}, publish_source=publish_source
    )
    print("Contract deployed to {}".format(fund_me.address))


def main():
    deploy_fund_me()
