// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract FundMe{
    using SafeMath for uint256;

    // Specifically, payable with ETH/Ethereum
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address _owner;
    constructor() {
        _owner = msg.sender;
    }

    function fund() public payable {
        // Getting External Data with Chainlink
        // what the ETH -> USD conversion rate

        // min value $50
        uint256 minimumUsd = 50 * 10 ** 18;

        // if(msg.value < minimumUsd){
        //     revert?
        // }

        require(getConversionRate(msg.value) >= minimumUsd, "You need to spend more ETH!");

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function withdraw() public payable onlyOwner{
        // msg.sender.transfer(address(this).balance);
        // only want the contract admin/owner
        // require msg.sender == "owner"
        address payable sender = payable (msg.sender);
        sender.transfer(address(this).balance);

        for(uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        funders = new address[](0);
    }

    modifier onlyOwner{
        require(msg.sender == _owner);
        _;
    }

    function getVersion() public view returns(uint256){
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }

    function getPrice() public view returns(uint256){
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);

        (,int256 answer,,,) =  priceFeed.latestRoundData();

        return uint256(answer * (10 ** 10));
    }

    // EthAmount in Gwei. Ex: 1000000000
    function getConversionRate(uint256 ethAmount) public view returns(uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / (10 ** 18);
        return ethAmountInUsd;
    }
}