from brownie import network, accounts, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["ganache-local", "development"]

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])