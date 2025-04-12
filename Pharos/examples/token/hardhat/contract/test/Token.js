const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Token", function () {
    let Token, token, owner, addr1;

    beforeEach(async function () {
        [owner, addr1] = await ethers.getSigners();

        Token = await ethers.getContractFactory("Token");
        token = await Token.deploy(ethers.parseEther("1000000"));
    });

    it("Should have the correct initial supply", async function () {
        const totalSupply = await token.totalSupply();
        expect(ethers.formatEther(totalSupply)).to.equal("1000000.0");
    });

    it("Should transfer tokens between accounts", async function () {
        await token.transfer(addr1.address, ethers.parseEther("100"));
        const balance = await token.balanceOf(addr1.address);
        expect(ethers.formatEther(balance)).to.equal("100.0");
    });
});
