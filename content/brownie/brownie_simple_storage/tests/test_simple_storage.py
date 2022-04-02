from brownie import accounts, SimpleStorage


def test_simple_storage_deploy():
    # Arrange
    account = accounts[0]

    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0

    # Assert
    assert starting_value == expected


def test_simple_storage_update():
    account = accounts[0]
    simple_storage = SimpleStorage[-1]

    expected = 200
    simple_storage.store(expected, {"from": account}).wait(1)

    assert simple_storage.retrieve() == expected
