from scripts.utils import LOCAL_BLOCKCHAIN_ENVINROMENTS
from scripts.utils import get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest

# Tests basic fund/withdraw functionality
def test_fund_withdraw():
    account = get_account()
    fundMe = deploy_fund_me()
    entranceFee = fundMe.entranceFee() + 100
    tx = fundMe.fund({"from": account, "value": entranceFee})
    tx.wait(1)
    assert fundMe.addressToFundAmount(account.address) == entranceFee
    tx2 = fundMe.withdraw({"from": account})
    tx2.wait(1)
    assert fundMe.addressToFundAmount(account.address) == 0


# Tests that only owner can withdraw funds
def test_owner_only_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVINROMENTS:
        pytest.skip("Only for local testing")

    fundMe = deploy_fund_me()
    entranceFee = fundMe.entranceFee()
    # not owner
    notOwner = accounts.add()
    tx = fundMe.fund({"from": notOwner, "value": entranceFee})
    tx.wait(1)
    # assert other accounts can fund address
    assert fundMe.addressToFundAmount(notOwner.address) == entranceFee
    # assert other accounts can't withdraw
    with pytest.raises(exceptions.VirtualMachineError):
        fundMe.withdraw({"from": notOwner})
