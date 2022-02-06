from cmath import exp
from brownie import SimpleStorage, accounts

def test_deploy():
    # Arrange
    account = accounts[0]
   
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.Retrieve()
    expected = 0
   
    # Assert
    assert starting_value == expected

def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    
    # Act
    simple_storage.Store(15, {"from": account})
    stored_value = simple_storage.Retrieve()
    expected = 15

    # Assert
    assert stored_value == expected

# Tips
# -k func_name
# --pdb
# -s 