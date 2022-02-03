// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage{
    uint256 _favoriteNumber;
    
    Person _person;

    Person[] _people;

    mapping(string => uint256) public PeopleDict;

    function Store(uint256 favoriteNumber_) public{
        _favoriteNumber = favoriteNumber_;
    }

    function Retrieve() public view returns(uint256){
        return _favoriteNumber;
    }

    function SetPerson(string memory name_, uint256 favoriteNumber_) public{
        _person = Person({name: name_, favoriteNumber: favoriteNumber_});
    }

    function GetPerson() public view returns(Person memory){
        return _person;
    }

    function AddPerson(string memory name_, uint256 favoriteNumber_) public{
        _people.push(Person({name: name_, favoriteNumber: favoriteNumber_}));
    }

    function GetPersonByIndex(uint256 index) public view returns(Person memory){
        return _people[index];
    }

    function AddFavoriteNumber(string memory name_, uint256 favoriteNumber_) public{
        PeopleDict[name_] = favoriteNumber_;
    }

    struct Person{
        string name;
        uint256 favoriteNumber;
    }
}