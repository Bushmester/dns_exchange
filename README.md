# What is DeFinitely Not Scam Exchange?

It is a console based cryptocurrency exchange simulation that uses sockets.

# Definitions
- **Seed phrase** is a string consisting of 6 random english words. It's generated during account creation, unique for every user and can not be changed! Seed phrase is used to import an account.
- **Hash address** is a unique string in the _0x\*\*\*\*\*\*\*\*_ format, where * can be replaced with any [a-f] or [0-9] symbol. It's generated during account creation, unique for every user and can not be changed! Hash address is used to define public account's name.
- **To import account** is to simply log in to it with using seed phrase.

# Commands

## Account

### 1. `create_account`

Creates new account.

Example:
```
create_account

New account has been successfully created!
address: 0x2387hf82
seed_phrase: red garden awesome run chocolate nice
```

### 2. `import_account`

Checks if there is account with the given `seed_phrase`, if yes: logs in, if not: shows an error.

Required arguments:
- `seed_phrase` (flags: `-sp`, `--seed-phrase`; type: `str`) - seed phrase (consists from 6 random english words).

Example:
```
import_account -sp red garden awesome run chocolate nice

Account has been successfully imported!
```

### 3. `my_account` _(auth required)_

Displays current account's info.

Example:
```
my_account

address: 0x2387hf82
```

### 4. `account_info`

Displays account info by it's address. Shown info: assets and last `number` transactions.

Required arguments:
- `address` (flags: `-a`, `--address`; type: `str`) - unique account's address.

Optional arguments:
- `number` (flags: `-n`, `--number`; type: `int`; default: `10`) - number of transactions to show.

Example:
```
account_info -a 0x2387hf82 -n 3

token   amount
BTC     3942.32
BNB     873.81
DNS     91.073

sender_address      receiver_address    token   amount
0x2387hf82          0x98238hgn          BTC     2498.298
0x2387hf82          0x2387hf82          DNS     32.026
0x2387hf82          0x2h4982h2          BNB     224.2396
```

## Token

### 1. `add_token` _(auth and admin rights required)_

Adds new tokens with the specified `tag` and `quantity` to address of the user who executed the command.

Required arguments:
- `tag` (flags: `-t`, `--tag`; type: `str`) - unique token tag.
- `quantity` (flags: `-q`, `--quantity`; type: `float`) - quantity of tokens to add.

Example:
```
add_token -t DNS -q 666

666 DNS tokens have been successfully added to your account's address!
```

### 2. `buy` _(auth required)_

Fills all suitable for `amount` and `exchange_rate` (if specified) sell orders for the first token of the `trading_pair`, then, if the amount of bought tokens is less than the specified `amount`, places a buy order.

Required arguments:
- `trading_pair` (flags: `-tp`, `--trading-pair`; type: `str`) - label of the trading pair.
- `amount` (flags: `-a`, `--amount`; type: `float`) - amount of tokens to buy.

Optional arguments:
- `exchange_rate` (flags: `-xr`, `--exchange-rate`; type: `float`) - amount of `token2` per one `token1`.

Example:
```
buy -tp BTC_DOGE -a 0.289 -xr 249838.36

Bought 0.14 BTC (249838.33 DOGE per 1 BTC)
Bought 0.0238 BTC (249838.36 DOGE per 1 BTC)
Placed 0.1252 BTC buy order (249838.36 DOGE per 1 BTC)
```

### 2. `sell` _(auth required)_

Fills all suitable for `amount` and `exchange_rate` (if specified) buy orders for the first token of the `trading_pair`, then, if the amount of bought tokens is less than the specified `amount`, places a sell order.

Required arguments:
- `trading_pair` (flags: `-tp`, `--trading-pair`; type: `str`) - label of the trading pair.
- `amount` (flags: `-a`, `--amount`; type: `float`) - amount of tokens to buy.

Optional arguments:
- `exchange_rate` (flags: `-xr`, `--exchange-rate`; type: `float`) - amount of `token2` per one `token1`.

Example:
```
sell -tp BTC_DOGE -a 0.289 -xr 249838.36

Sold 0.14 BTC (249838.39 DOGE per 1 BTC)
Sold 0.0238 BTC (249838.36 DOGE per 1 BTC)
Placed 0.1252 BTC sell order (249838.36 DOGE per 1 BTC)
```

## Pair

### 1. `add_pair` _(auth and admin rights required)_

Adds new trading pair with the `token1` + '_' + `token2` label to the list of the avaliable pairs.

Required arguments:
- `token1` (flags: `-t1`, `--token1`; type: `str`) - tag of the first token in pair.
- `token2` (flags: `-t2`, `--token2`; type: `str`) - tag of the second token in pair.

Example:
```
add_pair -t1 BTC -t2 DOGE

BTC_DOGE pair has been successfully added to the list of the avalialbe pairs!
```

### 2. `delete_pair` _(auth and admin rights required)_

Deletes trading pair with the given label from the list of the avaliable pairs.

Required arguments:
- `label` (flags: `-l`, `--label`; type: `str`) - label of the pair.

Example:
```
delete_pair -l BTC_DOGE

BTC_DOGE pair has been successfully removed from the list of the avalialbe pairs!
```

### 3. `list_pairs`

Displays the list of the avaliable trading pairs.

Optional arguments:
- `filter_by_label` (flags: `-f`, `--filter`; type: `str`) - string to filter by.

Example:
```
list_pairs -f BTC

label
BTC_DOGE
BTC_BNB
DNS_BTC
```

### 3. `pair_info`

Displays current buy and sell orders.

Required arguments:
- `label` (flags: `-l`, `--label`; type: `str`) - label of the pair.

Optional arguments:
- `number` (flags: `-n`, `--number`; type: `int`; default: `5`) - number of each buy/sell orders to show.


Example:
```
pair_info -l BTC_DOGE -n 3

SELL ORDERS
exchange_rate(DOGE)   amount(BTC)
249838.36             8.872
249838.32             3.12
249838.31             2.0982

BUY ORDERS
exchange_rate(DOGE)   amount(BTC)
249838.27             0.24
249838.15             13.971
249838.03             1.739
```

## Transaction

### 1. `list_transactions`

Displays recent `number` transactions (from all addresses).

Optional arguments:
- `number` (flags: `-n`, `--number`; type: `int`; default: `10`) - number of transactions to show.

Example:
```
list_transactions -n 3

sender_address      receiver_address    token   amount
0x2387hf82          0x98238hgn          BTC     2498.298
0x2h4982h2          0x2387hf82          DNS     32.026
0x98238hgn          0x2h4982h2          BNB     224.2396
```
