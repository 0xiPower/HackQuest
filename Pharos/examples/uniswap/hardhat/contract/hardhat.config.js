require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28",
  networks: {
    pharos: {
      url: "<PHAROS_RPC_URL>",
      accounts: [vars.get("PRIVATE_KEY")],
    },
  },
};
