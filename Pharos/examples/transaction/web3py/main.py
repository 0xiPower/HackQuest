from web3 import Web3

# Connect to Pharos Testnet
web3 = Web3(Web3.HTTPProvider("<PHAROS_RPC_URL>"))

# Your wallet private key (for testnet only, never expose this in production)
private_key = "Replace your private key"
account = web3.eth.account.from_key(private_key)

# Transaction details
tx = {
    "from": account.address,
    "to": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",  # Replace with the recipient's address
    "value": web3.to_wei(0.1, "ether"),  # Amount to send (0.1 PHAR)
    "gas": 21000,
    "gasPrice": web3.to_wei(1, "gwei"),
    "nonce": web3.eth.get_transaction_count(account.address),
}

# Sign and send the transaction
signed_tx = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("Transaction sent:", web3.to_hex(tx_hash))
