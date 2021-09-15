// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    //Can be replaced with OpenZepplin owner library
    address public owner;
    mapping(address => uint256) public addressToFundAmount;
    address[] public funders;
    uint256 public entranceFee = 50 * 10**18; //$50 minimum

    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function fund() public payable {
        require(getConversionRate((msg.value)) >= entranceFee, "Send more ETH");

        //stop duplicates in funders - all storage counts!
        if (addressToFundAmount[msg.sender] == 0) {
            funders.push(msg.sender);
        }
        addressToFundAmount[msg.sender] += msg.value;
    }

    function withdraw() public payable {
        require(msg.sender == owner);
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 i = 0; i < funders.length; i++) {
            addressToFundAmount[funders[i]] = 0;
        }
        funders = new address[](0);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 ethAmountInWei)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmountInWei) /
            1000000000000000000;
        return ethAmountInUsd;
    }
}
