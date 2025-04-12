const { ethers } = require("ethers");

// Connect to Pharos Testnet
const provider = new ethers.JsonRpcProvider("<PHAROS_RPC_URL>");

// Your wallet private key (for testnet only, never expose this in production)
const privateKey = "Replace your private key";
const wallet = new ethers.Wallet(privateKey, provider);

// Transaction details
const tx = {
    to: "0x742d35Cc6634C0532925a3b844Bc454e4438f44e", // Replace with the recipient's address
    value: ethers.parseEther("0.1"), // Amount to send (0.1 PHAR)
};

// Send the transaction
wallet.sendTransaction(tx)
    .then((transaction) => {
        console.log("Transaction sent:", transaction.hash);
    })
    .catch((error) => {
        console.error("Error sending transaction:", error);
    });
