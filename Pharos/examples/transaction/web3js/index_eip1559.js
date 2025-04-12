const Web3 = require("web3");

// Connect to Pharos Testnet
const web3 = new Web3.Web3("<PHAROS_RPC_URL>");

// Your wallet private key (for testnet only, never expose this in production)
const privateKey = "Replace your private key";
const account = web3.eth.accounts.privateKeyToAccount(privateKey);

// Transaction details
const tx = {
    from: account.address,
    to: "0x742d35Cc6634C0532925a3b844Bc454e4438f441", // Replace with the recipient's address
    value: web3.utils.toWei("0.1", "ether"), // Amount to send (0.1 PHAR)
    gas: 21000,  // Gas limit
    // gasPrice: web3.utils.toWei("10", "gwei"), // Gas price
    maxPriorityFeePerGas: web3.utils.toWei('2', 'gwei'),
    maxFeePerGas: web3.utils.toWei('30', 'gwei'),
    gas: 21000,
    chainId: 1,
};

// Sign and send the transaction
web3.eth.accounts.signTransaction(tx, privateKey)
    .then((signedTx) => {
        return web3.eth.sendSignedTransaction(signedTx.rawTransaction);
    })
    .then((receipt) => {
        console.log("Transaction sent:", receipt.transactionHash);
    })
    .catch((error) => {
        console.error("Error sending transaction:", error);
    });
