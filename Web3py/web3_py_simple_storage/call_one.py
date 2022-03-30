import json
from utils.loadConfig import loadConfig

# Load latest contract

with open("./data/latest_contract.json", "r") as file:
    latest_contract = json.loads(file.read())

with open("data/compiled_code.json", "r") as file:
    abi = json.loads(file.read())["contracts"]["SimpleStorage.sol"]["SimpleStorage"][
        "abi"
    ]


[w3, chain_id, my_address, private_key] = loadConfig()

# -------------- Work with contract --------------

last_contract_address = latest_contract["contractAddress"]

# Get contract with address and load abi

simple_storage = w3.eth.contract(address=last_contract_address, abi=abi)

# Call

print(simple_storage.functions.retrieve().call())

print("✅ - Done")
