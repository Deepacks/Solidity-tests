from brownie import (
    Contract,
    network,
    accounts,
    config,
    MockV3Aggregator,
    VRFCoordinatorV2Mock,
)

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

DECIMALS = 8
INITIAL_VALUE = 20000000000
LINK_FEE = 250000000000000000
GAS_PRICE_LINK = 67000000000


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorV2Mock,
}


def get_contract(contract_name):
    """This function will get the contract addresses from the brownie config
    if defined, otherwise it will deploy a mock and return it.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract
    """

    def deploy_mocks(
        contract_type,
        decimals=DECIMALS,
        initial_value=INITIAL_VALUE,
        link_fee=LINK_FEE,
        gas_price_link=GAS_PRICE_LINK,
    ):
        account = get_account()
        print("Deploying mock...")
        if contract_type == MockV3Aggregator:
            contract_type.deploy(decimals, initial_value, {"from": account})
        if contract_type == VRFCoordinatorV2Mock:
            contract_type.deploy(link_fee, gas_price_link, {"from": account})

        print("Deployed")

    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks(contract_type)
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract
