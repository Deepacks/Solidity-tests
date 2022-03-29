// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0 <0.9.0;

import "./node_modules/@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) addressToAmountFounded;
    address[] funders;
    address owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Sender is not owner");
        _;
    }

    function getPrice() private view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConvertionRate(uint256 ethAmount)
        private
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUSD = (ethPrice * ethAmount) / 10**18;
        return ethAmountInUSD;
    }

    function fund() public payable {
        uint256 minimumUSD = 50 * (10**18);
        require(
            getConvertionRate(msg.value) > minimumUSD,
            "Minimum amount is 50 USD"
        );

        addressToAmountFounded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funderAddress = funders[funderIndex];
            addressToAmountFounded[funderAddress] = 0;
        }
        funders = new address[](0);
    }
}
