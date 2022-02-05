from itertools import chain
import solcx
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

solcx.install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Our Solidity

compiled_sol = solcx.compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {"content": simple_storage_file},
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": [
                        "abi", "metadata", "evm.bytecode", "evm.sourceMap"
                    ]
                }
            }
        }
    },
    solc_version = "0.6.0",
)

with open("complied_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

print(private_key)

# Craete the contract in python
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id, 
        "from": my_address,
        "nonce": nonce
    })
# 2. sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key = private_key)

# 3. send a transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# wait block confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Working with the contract
# Contract address
# ABI
simple_storage = w3.eth.contract(address = tx_receipt.contractAddress, abi = abi)

# 2 ways of interact:
# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change

# Initial value of favorite number
print(simple_storage.functions.Retrieve().call())

store_tx = simple_storage.functions.Store(15).buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1
})

signed_store_tx = w3.eth.account.sign_transaction(store_tx, private_key = private_key)

print("Updating contract...")
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)

store_tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")
print(store_tx_receipt)

print(simple_storage.functions.Retrieve().call())
