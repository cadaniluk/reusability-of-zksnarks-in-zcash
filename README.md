# README

Programs contained in this repository:

- `zcash.py`: given a user-specific API key in a file named `api-key`, connects to https://getblock.io/ and sends RPC commands and other custom commands
- `zcash-net`: starts multiple Zcash nodes simultaneously
- `zcash-cli`: provides the RPC interface to any of the nodes started by `zcash-net`
- `get-tx`: given a transaction ID, retrieves this transaction using the API at https://api.zcha.in.
- `zcash-send`: given the right input data, creates a transparent transaction on any of the nodes started by `zcash-net`

Data contained in this repository (all data obtained from the JoinSplit circuit as implemented using the bellman library):

- `joinsplit_r1cs.zip`: the circuit's R1CS constraints
- `joinsplit_r1cs_names.zip`: the R1CS constraints' names
- `joinsplit_aux_names.zip`: the auxiliary inputs' ("witnesses" or "secret inputs") names
- `joinsplit_prim_names.zip`: the primary inputs'  (or "public inputs") names
- `tx_fee_points_and_coeffs.zip`: files detailing the difference in inputs and outputs to the R1CS constraints as well as the coefficients of the $h(x)$ quotient with identical JoinSplits but `vpub_new` set to $0$ for one and and $1$ for the other. The `js1_` and `js2_` prefixes indicate which JoinSplit is referred to. `a` stands for left input, `b` for right input, `c` for output, `h` for the $h(x)$ quotient. `_points` refers to evaluations, `_coeffs` to coefficients of a polynomial.

The [zcash repository](https://github.com/zcash/zcash) is used as a submodule.
It needs to be built in order to use `zcash-net`, `zcash-cli`, and `zcash-send`.
