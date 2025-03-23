//!
//! Stylus Hello World
//!
//! The following contract implements the Counter example from Foundry.
//!
//! ```solidity
//! contract Counter {
//!     uint256 public number;
//!     function setNumber(uint256 newNumber) public {
//!         number = newNumber;
//!     }
//!     function increment() public {
//!         number++;
//!     }
//! }
//! ```
//!
//! The program is ABI-equivalent with Solidity, which means you can call it from both Solidity and Rust.
//! To do this, run `cargo stylus export-abi`.
//!
//! Note: this code is a template-only and has not been audited.
//!
// Only run this as a WASM if the export-abi feature is not set.
#![cfg_attr(not(any(feature = "export-abi", test)), no_main)]
extern crate alloc;

// Modules and imports
mod erc20;

use crate::erc20::{Erc20, Erc20Params};
use alloy_primitives::{Address, U256};
use stylus_sdk::{
    call::{self, RawCall},
    function_selector, msg,
    prelude::*,
};

/// Immutable definitions
struct VaultParams;
impl Erc20Params for VaultParams {
    const NAME: &'static str = "Vault Example";
    const SYMBOL: &'static str = "VAULT";
    const DECIMALS: u8 = 18;
}

// Define the entrypoint as a Solidity storage object. The sol_storage! macro
// will generate Rust-equivalent structs with all fields mapped to Solidity-equivalent
// storage slots and types.
sol_storage! {
    #[entrypoint]
    struct Vault {
        address asset;
        uint totalSupply;
        // Allows erc20 to access StylusToken's storage and make calls
        #[borrow]
        Erc20<VaultParams> erc20;
    }
}

#[public]
#[inherit(Erc20<VaultParams>)]
impl Vault {
    pub fn setAsset(&mut self, _asset: Address) -> Result<Address, Vec<u8>> {
        self.asset.set(_asset);
        Ok(_asset)
    }

    #[payable]
    pub fn deposit(&mut self, amount: U256) -> Result<(), Vec<u8>> {
        let selector = function_selector!("transferFrom(address,address,uint256)");
        let data = [
            &selector[..],
            &msg::sender().into_array(),
            &self.asset.get().into_array(),
            &amount.to_be_bytes::<32>(),
        ].concat();
        RawCall::new().call(self.asset.get(), &data);
        let supply = self.totalSupply.get();
        let shares = if supply == U256::ZERO {
            amount
        } else {
            amount.checked_mul(supply).ok_or("Overflow")?.checked_div(self.totalAssets()?).ok_or("Divide by zero")?
        };
        self.erc20.mint(msg::sender(), shares);
        Ok(())
    }
    pub fn withdraw(&mut self, amount: U256) -> Result<(), Vec<u8>> {
        let supply = self.totalSupply.get();
        let shares = if supply == U256::ZERO {
            amount
        } else {
            amount.checked_mul(supply).ok_or("Overflow")?.checked_div(self.totalAssets()?).ok_or("Divide by zero")?
        };
        self.erc20.burn(msg::sender(), shares)?;
        call::transfer_eth(msg::sender(), amount)
    }

    pub fn asset(&self) -> Result<Address, Vec<u8>> {
        Ok(self.asset.get())
    }

    pub fn totalAssets(&self) -> Result<U256, Vec<u8>> {
        Ok(self.totalSupply.get())
    }
}
