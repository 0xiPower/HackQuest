// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules");

module.exports = buildModule("TokenModule", (m) => {
  const initialSupply = m.getParameter("initialSupply", 1_000_000n);
  const token = m.contract("Token", [initialSupply]);

  return { token };
});

