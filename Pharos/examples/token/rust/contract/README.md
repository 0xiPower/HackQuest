# Quick Start

## Install WASM Toolchains With Cargo

Install [Rust](https://www.rust-lang.org/tools/install), and then install the plugin using the Cargo tool:

```shell
cargo install --git https://github.com/PharosNetwork/pharos-cargo-stylus
```

Add the `wasm32-unknown-unknown` build target to your Rust compiler:

```shell
rustup target add wasm32-unknown-unknown
```

You should now have it available as a Cargo subcommand:

```shell
cargo stylus --help

Cargo subcommand for developing Pharos Stylus projects
```

## Build the Contract

```shell
cargo stylus check
```

## Deploy the Contract

```shell
cargo stylus deploy --private-key=<YOUR_PRIVATE_KEY>
```
