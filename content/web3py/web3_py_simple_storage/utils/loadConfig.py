import os
from dotenv import load_dotenv
from web3 import HTTPProvider, Web3

load_dotenv()


def loadConfig():

    w3 = Web3(HTTPProvider(os.getenv("HTTP_PROVIDER")))
    chain_id = int(os.getenv("CHAIN_ID"))
    my_address = os.getenv("ADDRESS")
    private_key = os.getenv("PRIVATE_KEY")

    return [w3, chain_id, my_address, private_key]
