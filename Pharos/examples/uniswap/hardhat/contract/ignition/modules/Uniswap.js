// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules");

module.exports = buildModule("UniswapModule", (m) => {
  const tokenA = m.contract("MockERC20", ["TokenA", "TKA"], { id: "TokenA" });
  const tokenB = m.contract("MockERC20", ["TokenB", "TKB"], { id: "TokenB" });

  const uniswap = m.contract("Uniswap", [tokenA, tokenB]);

  return { tokenA, tokenB, uniswap };
});
