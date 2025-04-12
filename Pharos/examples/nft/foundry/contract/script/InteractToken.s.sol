// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";
import "../src/Token.sol";

contract InteractToken is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        Token nft = Token(address(0x00)); // Replace with your NFT contract address

        // Mint a new NFT to the deployer's address
        uint256 tokenId = nft.mint(address(0x112233));
        console.log("Minted NFT with token ID:", tokenId);

        vm.stopBroadcast();
    }
}
