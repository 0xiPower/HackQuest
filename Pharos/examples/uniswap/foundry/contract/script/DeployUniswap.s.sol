// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";
import "../src/Uniswap.sol";
import "../test/Uniswap.t.sol";

contract DeployUniswap is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        MockERC20 tokenA = new MockERC20("TokenA", "TKA");
        MockERC20 tokenB = new MockERC20("TokenB", "TKB");

        Uniswap uniswap = new Uniswap(address(tokenA), address(tokenB));

        console.log("TokenA deployed at:", address(tokenA));
        console.log("TokenB deployed at:", address(tokenB));
        console.log("Uniswap deployed at:", address(uniswap));

        vm.stopBroadcast();
    }
}
