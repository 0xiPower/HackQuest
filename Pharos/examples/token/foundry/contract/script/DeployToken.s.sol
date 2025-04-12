// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import {Token} from "../src/Token.sol";

contract DeployToken is Script {
    Token public token;

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        token = new Token(1000000); // Initial supply of 1,000,000 tokens

        vm.stopBroadcast();
    }
}
