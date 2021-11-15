# What is DeFinitely Not Scam Exchange?

It is a console based cryptocurrency exchange simulation that uses sockets.

# Features

1. Seed phrases
2. Hash addresses
3. Open history of transactions and account assets info
4. 0.1% commission for all user operations

# Commands

## Account

### 1. `create_account`

Creates new account.

Example:
```
create_account

New account is created!
address: 0x2387hf823u
seed_phrase: red garden awesome run chocolate nice
```

### 2. `import_account`

Checks if there is account with the given `seed_phrase`, if yes: logs in, if not: shows an error.

Required arguements:
`seed_phrase` (flags: `-sp`, `--seed_phrase`; type: `str`) - seed phrase (consists from 6 random english words).

Example:
```
import_account -sp red garden awesome run chocolate nice

Account has been successfully imported!
```

### 3. `my_account` _(auth required)_

Displays account's info.

Example:
```
my_account

address: 0x2387hf823u
```

### 4. `account_info`

Displays account info by it's address. Shown info: assets and last `number` transactions.

Required arguements:
`address` (flags: `-a`, `--address`; type: `str`) - unique account's address.

Optional arguements:
`number` (flags: `-n`, `--number`; type: `int`; default: `10`) - number of transactions to show.

Example:
```
info -a 0x2387hf823u

token_tag       amount
BTC             3942.32
BNB             873.81
DNS             91.073

sender_address      receiver_address    token_tag   count
0x2387hf823u        0x98238hgn3g        BTC         2498.298
0x2387hf823u        0x2387hf823u        DNS         32.026
0x2387hf823u        0x2h4982h294        BNB         224.2396
```

## Token

### 1. `add_token` _(auth and admin rights required)_

Adds new tokens with the specified `tag` and `quantity` to address of the user who executed the command.

Required arguements:
`tag` (flags: `-t`, `--tag`; type: `str`) - unique token tag.
`quantity` (flags: `-q`, `--quantity`; type: `float`) - quantity of tokens to add.

Example:
```
add_token -t DNS -q 666

666 DNS tokens have been successfully added to your account's address!
```

### 2. `buy` _(auth required)_

Fills all suitable for `amount` and `exchange_rate` (if specified) sell orders for \*_token_1_tag_\* token, then, if the amount of bought tokens is less than the specified `amount`, places a buy order.

Required arguements:
- `trading_pair` (flags: `-tp`, `--trading_pair`; type: `str`) - label of the trading pair (in \*_token_1_tag_\* + '_' + \*_token_2_tag_\* format).
- `amount` (flags: `-a`, `--amount`; type: `float`) - amount of \*_token_1_tag_\* tokens to buy.

Optional arguements:
- `exchange_rate` (flags: `-xr`, `--exchange_rate`; type: `float`) - amount of \*_token_2_tag_\* tokens per one \*_token_1_tag_\* token.

Example:
```
buy -tp BTC_DOGE -a 0.289 -xr 249838.36

Bought 0.14 BTC (249838.33 DOGE per 1 BTC)
Bought 0.0238 BTC (249838.36 DOGE per 1 BTC)
Placed 0.1252 BTC buy order (249838.36 DOGE per 1 BTC)
```

### 3. `sell` _(auth required)_

Fills all suitable for `amount` and `exchange_rate` (if specified) buy orders for \*_token_1_tag_\* token, then, if the amount of sold tokens is less than the specified `amount`, places a sell order.

Required arguements:
- `trading_pair` (flags: `-tp`, `--trading_pair`; type: `str`) - label of the trading pair (in \*_token_1_tag_\* + '_' + \*_token_2_tag_\* format).
- `amount` (flags: `-a`, `--amount`; type: `float`) - amount of \*_token_1_tag_\* tokens to sell.

Optional arguements:
- `exchange_rate` (flags: `-xr`, `--exchange_rate`; type: `float`) - amount of \*_token_2_tag_\* tokens per one \*_token_1_tag_\* token.

Example:
```
sell -tp BTC_DOGE -a 0.289 -xr 249838.36

Sold 0.14 BTC (249838.39 DOGE per 1 BTC)
Sold 0.0238 BTC (249838.36 DOGE per 1 BTC)
Placed 0.1252 BTC sell order (249838.36 DOGE per 1 BTC)
```

## Pair

### 1. `add_pair` _(auth and admin rights required)_

Adds new trading pair with the \*_token_1_tag_\* + '_' + \*_token_2_tag_\* label to the list of the avaliable pairs.

Required arguements:
`token1` (flags: `-t1`, `--token1`; type: `str`) - tag of the first token in pair.
`token2` (flags: `-t2`, `--token2`; type: `str`) - tag of the second token in pair.

Example:
```
add_pair -t1 BTC -t2 DOGE

BTC_DOGE pair has been successfully added to the list of the avalialbe pairs!
```

### 2. `delete_pair` _(auth and admin rights required)_

Deletes trading pair with the \*_token_1_tag_\*` + '_' + \*_token_2_tag_\* label from the list of the avaliable pairs.

Required arguements:
`token1` (flags: `-t1`, `--token1`; type: `str`) - tag of the first token in pair.
`token2` (flags: `-t2`, `--token2`; type: `str`) - tag of the second token in pair.

Example:
```
delete_pair -t1 BTC -t2 DOGE

BTC_DOGE pair has been successfully removed from the list of the avalialbe pairs!
```

### 3. `list_pairs` _(auth required)_

Displays the list of the avaliable trading pairs.

Example:
```
list_pairs

label
BTC_DOGE
BTC_BNB
BTC_TWT
DNS_DOGE
DNS_BNB
```

## Transaction

### 1. `list_transactions`

Displays recent `number` transactions (from all addresses).

Optional arguements:
`number` (flags: `-n`, `--number`; type: `int`; default: `10`) - number of transactions to show.

Example:
```
scan_transactions -n 3

sender_address      receiver_address    token_tag   count
0x2387hf823u        0x98238hgn3g        BTC         2498.298
0x2h4982h294        0x2387hf823u        DNS         32.026
0x98238hgn3g        0x2h4982h294        BNB         224.2396
```
