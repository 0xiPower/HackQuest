const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Uniswap", function () {
    let Uniswap, uniswap, TokenA, tokenA, TokenB, tokenB, user;

    beforeEach(async function () {
        [user] = await ethers.getSigners();

        const TokenFactory = await ethers.getContractFactory("MockERC20");
        tokenA = await TokenFactory.deploy("TokenA", "TKA");
        tokenB = await TokenFactory.deploy("TokenB", "TKB");

        const UniswapFactory = await ethers.getContractFactory("Uniswap");
        uniswap = await UniswapFactory.deploy(tokenA.target, tokenB.target);

        await tokenA.mint(user.address, 1000);
        await tokenB.mint(user.address, 1000);
    });

    it("Should add liquidity", async function () {
        await tokenA.connect(user).approve(uniswap.target, 100);
        await tokenB.connect(user).approve(uniswap.target, 100);

        await uniswap.connect(user).addLiquidity(100, 100);

        const reserveA = await uniswap.reserveA();
        const reserveB = await uniswap.reserveB();
        expect(reserveA).to.equal(100, "Reserve A should be 100");
        expect(reserveB).to.equal(100, "Reserve B should be 100");
    });

    it("Should remove liquidity", async function () {
        await tokenA.connect(user).approve(uniswap.target, 100);
        await tokenB.connect(user).approve(uniswap.target, 100);
        await uniswap.connect(user).addLiquidity(100, 100);

        await uniswap.connect(user).removeLiquidity(50, 50);

        const reserveA = await uniswap.reserveA();
        const reserveB = await uniswap.reserveB();
        expect(reserveA).to.equal(50, "Reserve A should be 50");
        expect(reserveB).to.equal(50, "Reserve B should be 50");
    });

    it("Should swap token A for token B", async function () {
        await tokenA.connect(user).approve(uniswap.target, 100);
        await tokenB.connect(user).approve(uniswap.target, 100);
        await uniswap.connect(user).addLiquidity(100, 100);

        await tokenA.connect(user).approve(uniswap.target, 10);
        await uniswap.connect(user).swapAToB(10);

        const reserveA = await uniswap.reserveA();
        const reserveB = await uniswap.reserveB();
        expect(reserveA).to.equal(110, "Reserve A should be 110");
        expect(reserveB).to.equal(90, "Reserve B should be 90");
    });
});
