// SPDX-License-Identifier: MIT

pragma solidity 0.8.11;

import "./SimpleStorage.sol";

contract StorageFactory is SimpleStorage {
    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorage() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    function sfStore(
        uint256 _simpleStorageIndex,
        string memory _name,
        uint256 _favoriteNumber
    ) public {
        SimpleStorage simpleStorage = SimpleStorage(
            address(simpleStorageArray[_simpleStorageIndex])
        );
        simpleStorage.addPerson(_name, _favoriteNumber);
    }

    function sfRetrieve(uint256 _simpleStorageIndex, string memory _name)
        public
        view
        returns (uint256)
    {
        SimpleStorage simpleStorage = SimpleStorage(
            address(simpleStorageArray[_simpleStorageIndex])
        );
        return simpleStorage.retrievePerson(_name);
    }
}
