// SPDX-License-Identifier: MIT

pragma solidity ^0.8.11;

contract SimpleStorage {
    uint256 favoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    mapping(string => uint256) private nameToFavoriteNumber;

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    function retrievePerson(string memory _name) public view returns (uint256) {
        return nameToFavoriteNumber[_name];
    }
}
