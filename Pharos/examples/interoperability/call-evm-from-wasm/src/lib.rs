#![cfg_attr(not(feature = "export-abi"), no_main)]
extern crate alloc;

use stylus_sdk::{
    abi::Bytes,
    alloy_primitives::{Address, U256},
    prelude::*,
    stylus_core::calls::context::Call,
};
use alloy_sol_types::{sol, SolCall};

sol! {
    interface IErc20  {
        function mint(uint256 value) external;
    }
}

#[storage]
#[entrypoint]
pub struct Interoperability;

#[public]
impl Interoperability {
    /// Here we can call an EVM contract with the given target address and calldata.
    pub fn execute(&self, target: Address, data: Bytes) -> Bytes {
        let result = self.vm().call(&Call::default(), target, &data);
        result.unwrap().into()
    }

    /// Here we can transfer ETH to the given target address.
    pub fn transfer_eth(&self, to: Address, amount: U256) -> Result<(), Vec<u8>> {
        self.vm().transfer_eth(to, amount)
    }

    /// Here we call an ERC20 token contract written in Solidity.
    pub fn mint_erc20(&self, erc20: Address, value: U256) -> Bytes {
        self.execute(erc20, Bytes(IErc20::mintCall {
            value,
        }.abi_encode()))
    }
}
