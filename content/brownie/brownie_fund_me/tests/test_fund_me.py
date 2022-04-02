import pytest
from brownie import FundMe, accounts, network, exceptions

from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me


def test_fund_me_deploy():
    deploy_fund_me()

    assert len(FundMe) == 1


def test_fund_me_fund():
    account = get_account()
    fund_me = FundMe[-1]
    entrance_fee = fund_me.getEntranceFee()

    tx = fund_me.fund({"from": account, "value": entrance_fee + 1})
    tx.wait(1)

    assert fund_me.addressToAmountFounded(account.address) == entrance_fee + 1


def test_fund_me_withdraw():
    account = get_account()
    fund_me = FundMe[-1]

    tx = fund_me.withdraw({"from": account})
    tx.wait(1)

    assert fund_me.addressToAmountFounded(account.address) == 0


def test_only_owner_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = FundMe[-1]
    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
