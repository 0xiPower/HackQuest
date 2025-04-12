// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {HackQuestNFT} from "../src/HackQuestNFT.sol";

contract HackQuestNFTTest is Test {
    HackQuestNFT public hackQuestNFT;
    HackQuestNFT public participantNFT;

    function setUp() public {
        hackQuestNFT = new HackQuestNFT("HackQuest", "HQ");
    }

    function test_Mint() public {
        address alice = address(1);
        vm.startPrank(alice);
        participantNFT = new HackQuestNFT("AlicePharos", "AP");
        hackQuestNFT.mint(address(participantNFT));
        uint256 aliceBal = hackQuestNFT.balanceOf(alice);
        assertEq(aliceBal, 1);
        vm.stopPrank();
    }

    function test_ReaptMint() public {
        address alice = address(1);
        vm.startPrank(alice);
        participantNFT = new HackQuestNFT("AlicePharos", "AP");
        hackQuestNFT.mint(address(participantNFT));
        
        // 测试重复铸造会失败
        vm.expectRevert(abi.encodeWithSelector(HackQuestNFT.AlreadyMint.selector, alice, address(participantNFT)));
        hackQuestNFT.mint(address(participantNFT));

        vm.stopPrank();
    }

    function test_TokenURI() public {
        address alice = address(1);
        vm.startPrank(alice);
        participantNFT = new HackQuestNFT("AlicePharos", "AP");
        hackQuestNFT.mint(address(participantNFT));
        
        string memory uri = hackQuestNFT.tokenURI(1);
        console.log(uri);
         vm.stopPrank();
    }
}