// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

contract FundMe {
    mapping(address => uint256) public addressToAmountFounded;

    function fund() public payable {
        addressToAmountFounded[msg.sender] += msg.value;
    }
}
