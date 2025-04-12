import React, { useState } from "react";
import { ethers } from "ethers";

const contractAddress = "YOUR_CONTRACT_ADDRESS"; // Replace with your contract address
const abi = [
    {
        "inputs": [],
        "name": "get",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "x",
                "type": "uint256"
            }
        ],
        "name": "set",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
];

function App() {
    const [value, setValue] = useState("");
    const [storedValue, setStoredValue] = useState("");

    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const contract = new ethers.Contract(contractAddress, abi, signer);

    const handleSet = async () => {
        await contract.set(value);
        alert("Value set!");
    };

    const handleGet = async () => {
        const result = await contract.get();
        setStoredValue(result.toString());
    };

    return (
        <div>
            <h1>Simple Storage dApp</h1>
            <input
                type="text"
                value={value}
                onChange={(e) => setValue(e.target.value)}
                placeholder="Enter a value"
            />
            <button onClick={handleSet}>Set Value</button>
            <button onClick={handleGet}>Get Value</button>
            <p>Stored Value: {storedValue}</p>
        </div>
    );
}

export default App;
