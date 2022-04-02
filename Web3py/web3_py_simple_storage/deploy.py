import json
from solcx import compile_standard

from utils.hexJsonEncoder import HexJsonEncoder
from utils.loadConfig import loadConfig

with open("contracts/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Solidity to json file

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.11",
)

with open("data/compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get bytecode

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get abi

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Load config and connect to blockchain

[w3, chain_id, my_address, private_key] = loadConfig()

# Create contract

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction

nonce = w3.eth.getTransactionCount(my_address)

# 1. Build transaction

tx = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

# 2. Sign transaction

signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)

# 3. Send transaction

print("Deploying contract...")
print("etherscan: https://rinkeby.etherscan.io/tx/{}".format(signed_tx.hash.hex()))
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Receive confirmation

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Dump transaction receipt

with open("data/latest_contract.json", "w") as file:
    json.dump(dict(tx_receipt), file, cls=HexJsonEncoder)


print("✅ - Done")
