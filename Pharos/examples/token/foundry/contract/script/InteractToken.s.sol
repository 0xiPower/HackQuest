// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import {Token} from "../src/Token.sol";

contract InteractMyToken is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        Token token = Token(address(0x00)); // Replace with your token contract address
        console.log("sender:", msg.sender);
        // Check balance
        uint256 balance = token.balanceOf(msg.sender);
        console.log("Balance:", balance);

        // Transfer tokens
        bool result = token.transfer(address(0x112233), 100); // Replace with recipient address and amount
        console.log("Tokens transferred", result);

        uint256 user1Balance = token.balanceOf(address(0x112233));
        console.log("user balance", user1Balance);

        vm.stopBroadcast();
    }
}
