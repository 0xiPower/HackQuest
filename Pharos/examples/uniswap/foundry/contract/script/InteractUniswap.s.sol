// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";
import "../src/Uniswap.sol";
import "../test/Uniswap.t.sol";

contract InteractUniswap is Script {
    function run() external {
        address tokenAAddress = address(0x0A);
        address tokenBAddress = address(0x0B);
        address uniswapAddress = address(0xFF);

        MockERC20 tokenA = MockERC20(tokenAAddress);
        MockERC20 tokenB = MockERC20(tokenBAddress);
        Uniswap uniswap = Uniswap(uniswapAddress);

        address user = address(0x123);

        tokenA.mint(user, 1000);
        tokenB.mint(user, 1000);

        vm.prank(user);
        tokenA.approve(address(uniswap), 100);

        vm.prank(user);
        tokenB.approve(address(uniswap), 100);

        vm.prank(user);
        uniswap.addLiquidity(100, 100);
        console.log("Liquidity added");

        vm.prank(user);
        tokenA.approve(address(uniswap), 10);

        vm.prank(user);
        uniswap.swapAToB(10);
        console.log("Swapped TokenA for TokenB");

        vm.prank(user);
        uniswap.removeLiquidity(50, 50);
        console.log("Liquidity removed");
    }
}
