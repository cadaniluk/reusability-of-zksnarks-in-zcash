# README

Programs contained in this repository:

- `zcash.py`: given a user-specific API key in a file named `api-key`, connects to https://getblock.io/ and sends RPC commands and other custom commands
- `zcash-net`: starts multiple Zcash nodes simultaneously
- `zcash-cli`: provides the RPC interface to any of the nodes started by `zcash-net`
- `get-tx`: given a transaction ID, retrieves this transaction using the API at https://api.zcha.in.
- `zcash-send`: given the right input data, creates a transparent transaction on any of the nodes started by `zcash-net`

The [zcash repository](https://github.com/zcash/zcash) is used as a submodule.
It needs to be built in order to use `zcash-net`, `zcash-cli`, and `zcash-send`.
