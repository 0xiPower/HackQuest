// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.22;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";

contract HackQuestNFT is ERC721 {

    bytes4 private constant _INTERFACE_ID_ERC721 = 0x80ac58cd;

    using EnumerableSet for EnumerableSet.AddressSet;
    EnumerableSet.AddressSet private participants;
    EnumerableSet.AddressSet private participantContracts;

    uint256 public nftId;

    error NotContract(address contractAddr);

    error NotNFTContract(address contractAddr);

    error AlreadyMint(address minter, address contractAddr);

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {}

    function mint(address yourNft) public returns (uint256) {
        require(!participants.contains(msg.sender) && !participantContracts.contains(yourNft), AlreadyMint(msg.sender, yourNft));

        require(yourNft.code.length>0, NotContract(yourNft));

        ERC721 participantContract = ERC721(yourNft);
        bool flag = participantContract.supportsInterface(_INTERFACE_ID_ERC721);
        require(flag, NotNFTContract(yourNft));


        nftId += 1;
        _mint(msg.sender, nftId);

        participants.add(msg.sender);
        participantContracts.add(yourNft);
        return nftId;
    }


    function _baseURI() internal pure override returns (string memory) {
        return "ipfs://bafybeiffw5q6qlg7gcrqtkbb6ttykptsnhpxafg6k4ouaxbo5xrrfu4djm/";
    }

    function allParticipants() public view returns (address[] memory) {
        return participants.values();
    }

    function allParticipantContracts() public view returns (address[] memory) {
        return participantContracts.values();
    }

}