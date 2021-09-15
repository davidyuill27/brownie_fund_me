from scripts.utils import LOCAL_BLOCKCHAIN_ENVINROMENTS, get_account, deployMocks
from brownie import accounts, network, config, FundMe, MockV3Aggregator


def deploy_fund_me():
    account = get_account()
    print(f"active network is: " + network.show_active())
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVINROMENTS:
        # live contract address
        priceFeedAddress = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deployMocks()
        priceFeedAddress = MockV3Aggregator[-1].address

    fundMe = FundMe.deploy(
        priceFeedAddress,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    return fundMe


def main():
    deploy_fund_me()
