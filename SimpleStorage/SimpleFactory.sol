// SPDX-License-Identifier: MIT

pragma solidity ^0.8.11;

import "./SimpleStorage.sol";

contract StorageFactory is SimpleStorage {
    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorage() public {
        simpleStorageArray.push(new SimpleStorage());
    }

    function sfStore(
        uint256 _simpleStorageIndex,
        string memory _name,
        uint256 _favoriteNumber
    ) public {
        SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]))
            .addPerson(_name, _favoriteNumber);
    }

    function sfRetrieve(uint256 _simpleStorageIndex, string memory _name)
        public
        view
        returns (uint256)
    {
        return
            SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]))
                .retrievePerson(_name);
    }
}
