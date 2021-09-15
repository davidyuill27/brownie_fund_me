from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

# variables
DECIMALS = 8
STARTING_PRICE = 20000000000000

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVINROMENTS = ["development", "ganache-local"]

# Util function to get account depending on network used
def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVINROMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.load("brownie")


# Deploys mocks (if not already)
def deployMocks():
    print("Deploying Mocks if needed...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
        )
        print("Mocks deployed...")
    else:
        print("Mock already exists")
