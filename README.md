# DeFinitely Not Scam Exchange is a console based cryptocurrency exchange simulation that uses sockets.

## Commands

### Token operations

#### 1. Command: `buy` _(auth required)_

Fills all suitable for `amount` and `exchange_rate` (if specified) sell orders, then, if the amount of bought tokens is less than the specified `amount`, places a buy order.

Required arguements:
- `token_to_buy` (flags: `-bt`, `--buy_token`; type: `str`) - tag of the token to buy.
- `amount` (flags: `-a`, `--amount`; type: `float`) - amount of \*_token_to_buy_\* tokens to buy.
- `token_to_sell` (flags: `-st`, `--sell_token`; type: `str`) - tag of the token to sell.

Optional arguements:
- `exchange_rate` (flags: `-xr`, `--exchange_rate`; type: `float`) - amount of \*_token_to_sell_\* tokens per one \*_token_to_buy_\* token.

<details>
  <summary>Example</summary>
    buy -bt BTC -n 0.289 -st DOGE -xr 249838.36<br><br>
    Bought 0.14 BTC (249838.33 DOGE per 1 BTC)<br>
    Bought 0.0238 BTC (249838.36 DOGE per 1 BTC)<br>
    Placed 0.1252 BTC buy order (249838.36 DOGE per 1 BTC)
</details>

#### 2. Command: `sell` _(auth required)_

Fills all suitable for `amount` and `exchange_rate` (if specified) buy orders, then, if the amount of sold tokens is less than the specified `amount`, places a sell order.

Required arguements:
- `token_to_sell` (flags: `-st`, `--sell_token`; type: `str`) - tag of the token to sell.
- `amount` (flags: `-a`, `--amount`; type: `float`) - amount of \*_token_to_sell_\* tokens to sell.
- `token_to_buy` (flags: `-bt`, `--buy_token`; type: `str`) - tag of the token to buy.

Optional arguements:
- `exchange_rate` (flags: `-xr`, `--exchange_rate`; type: `float`) - amount of \*_token_to_buy_\* tokens per one \*_token_to_sell_\* token.

<details>
  <summary>Example</summary>
    sell -st DOGE -n 72203.28 -bt BTC -xr 0.0000040<br><br>
    Sold 34977.37 DOGE (0.0000039 per 1 DOGE)<br>
    Sold 2343.89 DOGE (0.0000040 DOGE per 1 BTC)<br>
    Placed 34882.02 DOGE sell order (0.0000040 BTC per 1 DOGE)
</details>

#### 3. Command: `add` _(auth and admin rights required)_

Adds new tokens with the specified `tag` and `quantity` to address of the user who executed the command.

Required arguements:
`tag` (flags: `-t`, `--tag`; type: `str`) - unique token tag.
`quantity` (flags: `-q`, `--quantity`; type: `float`) - quantity of tokens to add.

<details>
  <summary>Example</summary>
    add -t DNS -a 666
</details>

#### 4. Command: `list` _(auth required)_

Shows all tokens.

<details>
  <summary>Example</summary>
    list

    tag       quantity
    BTC       283923.9897
    BNB       3209.36
    DOGE      283423289.617
    DNS       83429384.2938
</details>

### Account operations

#### 1. Command: `create_account`

Creates new account.

<details>
  <summary>Example</summary>
    create_account<br><br>
    New account is created!<br>
    address: 0x2387hf823u<br>
    seed_phrase: red garden awesome run chocolate nice
</details>

#### 2. Command: `import_account`

Checks if there is account with the given `seed_phrase`, if yes: logs in, if not: shows an error.

Required arguements:
`seed_phrase` (flags: `-sp`, `--seed_phrase`; type: `str`) - seed phrase (consists from 6 random english words).

<details>
  <summary>Example</summary>
    import_account -sp red garden awesome run chocolate nice<br><br>
    Successfully imported!
</details>

#### 3. Command: `scan_transactions`

Shows recent `number` transactions (from all addresses).

Optional arguements:
`number` (flags: `-n`, `--number`; type: `int`; default: `10`) - number of transactions to show.

<details>
  <summary>Example</summary>
    scan_transactions -n 3

    sender_address      receiver_address    token_tag   count
    0x2387hf823u        0x98238hgn3g        BTC         2498.298
    0x2h4982h294        0x2387hf823u        DNS         32.026
    0x98238hgn3g        0x2h4982h294        BNB         224.2396
</details>

#### 4. Command: `info`

Shows account info by it's address. Shown info: assets and last `number` transactions.

Required arguements:
`address` (flags: `-a`, `--address`; type: `str`) - unique account's address.

Optional arguements:
`number` (flags: `-n`, `--number`; type: `int`; default: `10`) - number of transactions to show.

<details>
  <summary>Example</summary>
    <br>info -a 0x2387hf823u<br><br>

    token_tag       amount
    BTC             3942.32
    BNB             873.81
    DNS             91.073
  
    sender_address      receiver_address    token_tag   count
    0x2387hf823u        0x98238hgn3g        BTC         2498.298
    0x2387hf823u        0x2387hf823u        DNS         32.026
    0x2387hf823u        0x2h4982h294        BNB         224.2396
</details>

#### 4. Command: `my_account`

Shows account's info.

<details>
  <summary>Example</summary>
    <br>my_account<br><br>
    0x2387hf823u
</details>

## Features

1. Seed phrases
2. Hash addresses
3. Open history of transactions and account assets info
4. 0.1% commission for all user operations
