// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/Token.sol";

contract TokenTest is Test {
    Token nft;
    address deployer = address(0x123);
    address user1 = address(0x456);

    function setUp() public {
        // Set up the deployer's private key
        vm.prank(deployer);

        // Deploy the NFT contract
        nft = new Token();
    }

    function testMint() public {
        // Mint a new NFT to user1
        vm.prank(deployer);
        uint256 tokenId = nft.mint(user1);

        // Check that user1 owns the NFT
        address owner = nft.ownerOf(tokenId);
        assertEq(owner, user1, "User1 should own the minted NFT");
    }
}
