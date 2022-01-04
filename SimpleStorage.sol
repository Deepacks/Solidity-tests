// SPDX-License-Identifier: MIT

pragma solidity ^0.8.11;

contract SimpleStorage {
    mapping(string => uint256) private nameToFavoriteNumber;

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    function retrievePerson(string memory _name) public view returns (uint256) {
        return nameToFavoriteNumber[_name];
    }
}
