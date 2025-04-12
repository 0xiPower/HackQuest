// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../src/Uniswap.sol";

contract MockERC20 is ERC20 {
    constructor(string memory name, string memory symbol) ERC20(name, symbol) {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }

    function mint(address to, uint256 amount) public {
        _mint(to, amount);
    }
}

contract UniswapTest is Test {
    Uniswap uniswap;
    MockERC20 tokenA;
    MockERC20 tokenB;
    address user = address(0x123);

    function setUp() public {
        // Deploy mock ERC20 tokens
        tokenA = new MockERC20("TokenA", "TKA");
        tokenB = new MockERC20("TokenB", "TKB");

        // Deploy Uniswap contract
        uniswap = new Uniswap(address(tokenA), address(tokenB));

        // Mint tokens to the user
        tokenA.mint(user, 1000);
        tokenB.mint(user, 1000);
    }

    function testAddLiquidity() public {
        // Approve Uniswap to spend tokens
        vm.prank(user);
        tokenA.approve(address(uniswap), 100);

        vm.prank(user);
        tokenB.approve(address(uniswap), 100);

        // Add liquidity
        vm.prank(user);
        uniswap.addLiquidity(100, 100);

        // Check reserves
        (uint256 reserveA, uint256 reserveB) = (uniswap.reserveA(), uniswap.reserveB());
        assertEq(reserveA, 100, "Reserve A should be 100");
        assertEq(reserveB, 100, "Reserve B should be 100");
    }

    function testRemoveLiquidity() public {
        // Add liquidity first
        vm.prank(user);
        tokenA.approve(address(uniswap), 100);

        vm.prank(user);
        tokenB.approve(address(uniswap), 100);

        vm.prank(user);
        uniswap.addLiquidity(100, 100);

        // Remove liquidity
        vm.prank(user);
        uniswap.removeLiquidity(50, 50);

        // Check reserves
        (uint256 reserveA, uint256 reserveB) = (uniswap.reserveA(), uniswap.reserveB());
        assertEq(reserveA, 50, "Reserve A should be 50");
        assertEq(reserveB, 50, "Reserve B should be 50");
    }

    function testSwapAToB() public {
        // Add liquidity first
        vm.prank(user);
        tokenA.approve(address(uniswap), 100);

        vm.prank(user);
        tokenB.approve(address(uniswap), 100);

        vm.prank(user);
        uniswap.addLiquidity(100, 100);

        // Swap token A for token B
        vm.prank(user);
        tokenA.approve(address(uniswap), 10);

        vm.prank(user);
        uniswap.swapAToB(10);

        // Check reserves
        (uint256 reserveA, uint256 reserveB) = (uniswap.reserveA(), uniswap.reserveB());
        assertEq(reserveA, 110, "Reserve A should be 110");
        assertEq(reserveB, 90, "Reserve B should be 90");
    }
}
