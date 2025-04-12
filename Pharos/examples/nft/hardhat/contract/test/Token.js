const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Token", function () {
    let token, deployer, user1;

    beforeEach(async function () {
        [deployer, user1] = await ethers.getSigners();
        const TokenFactory = await ethers.getContractFactory("Token");
        token = await TokenFactory.deploy();
    });

    it("Should mint a new token to user1", async function () {
        await token.connect(deployer).mint(user1.address);
        const owner = await token.ownerOf(1);
        expect(owner).to.equal(user1.address, "User1 should own the minted token");
    });
});
