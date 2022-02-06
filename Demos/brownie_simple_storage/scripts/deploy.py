from brownie import accounts, config, SimpleStorage, network
import os


def deploy_simple_storage():
    account = get_account()
    # account = accounts.load("testAccount")
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"])

    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)
    # simple_storage.wait(1)
    stored_value = simple_storage.Retrieve()
    print(stored_value)
    transaction = simple_storage.Store(15, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.Retrieve()
    print(updated_stored_value)

def get_account():
    if(network.show_active() == "development"):
        return accounts[0]
    
    return accounts.add(config["wallets"]["from_key"])

def main():
    deploy_simple_storage()