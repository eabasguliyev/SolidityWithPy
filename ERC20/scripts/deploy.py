from brownie import OurToken, config, network
from scripts.helpful_scripts import get_account
from web3 import Web3
def deploy():
    account = get_account()
    initial_supply = Web3.toWei(2000, "ether")
    our_token = OurToken.deploy(initial_supply, {"from": account},
            publish_source = config["networks"][network.show_active()].get("verify", False))

    print(f"Token deployed to {our_token.address}")


def main():
    deploy()