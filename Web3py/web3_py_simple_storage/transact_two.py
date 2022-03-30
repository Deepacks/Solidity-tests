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

# Transact

nonce = w3.eth.getTransactionCount(my_address)

store_tx = simple_storage.functions.addPerson("pino", 69).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_store_tx = w3.eth.account.sign_transaction(store_tx, private_key)

print("Updating contract...")
print(
    "etherscan: https://rinkeby.etherscan.io/tx/{}".format(signed_store_tx.hash.hex())
)
tx_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
send_store_tx = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Updated!")

print("tx receipt: ", send_store_tx)


print("✅ - Done")
