# What is DeFinitely Not Scam Exchange?
It is a console based toy cryptocurrency exchange that uses sockets. There is simulation of _seed phrases\*_, _hash addresses\*_, mining process, buy/sell orders, open transaction history and also 0.1% commission on each deal.

# Definitions
- **Auth token** is a token to define authenticated users. It's generated from account _seed phrase\*_ with using hash function.
- **Hash address** is a unique string in the _0x\*\*\*\*\*\*\*\*_ format, where \* is any [a-f] or [0-9] symbol. It's generated during account creation, unique for every user and can not be changed! Hash address is used to define public account's name.
- To **import account** is to simply log in to it with using _seed phrase\*_.
- **Mining number** is a number from 1 to 10, which is stored on the server. The first account who guesses mining number gets random (from 0.0 to 10.0) amount of DNS to his assets. After number is guessed, it changes.
- **Seed phrase** is a string consisting of 6 random english words. It's generated during account creation, unique for every user and can not be changed! Seed phrase is used to _import an account\*_.

# Protocol
Both `request` and `response` are JSON formatted utf-8 strings with _start;_ at the start and _end;_ at the end.

## Request

### Structure:

```
start;
{
    "auth_token": "auth_token_or_empty",
    "command": "command_name",
    "args": {
        "argument_1_name": "argument_1_value",
        "argument_2_name": "argument_2_value",
        ...
    }
}
end;
```

### Example:

On `account_info -a 0x2387af82 -n 3`:
```
start;
{
    "auth_token": "7h89thugnt0234thg9epwotjw49hoe4y",
    "command": "account_info",
    "args": {
        "address": "0x2387af82"
        "number": 3
    }
}
end;
```

## Response

### Structure:

```
start;
{
    "auth_token": "auth_token_or_empty",
    "content": [
        {
            "type": "text",
            "title": "Text title"
            "lines": [
                "Content text paragraph 1.",
                ...
            ]
        },
        {
            "type": "table",
            "name": "Table name",
            "headers": ["column_1_name", ...],
            "rows": [
                ["Row 1, column 1 value", ...],
                ...
            ]
        },
        ...
    ],
    "errors": [
        "Error message",
        ...
    ]
}
end;
```

### Examples:

On `sell -tp BTC_DOGE -a 0.289 -xr 249838.36`:
```
start;
{
    "auth_token": "7h89thugnt0234thg9epwotjw49hoe4y",
    "content": [
        {
            "type": "text",
            "title": "",
            "lines": [
                "Sold 0.14 BTC (249838.39 DOGE per 1 BTC)",
                "Sold 0.0238 BTC (249838.36 DOGE per 1 BTC)",
                "Placed 0.1252 BTC sell order (249838.36 DOGE per 1 BTC)"
            ]
        }
    ],
    "errors": []
}
end;
```

On `account_info -a 0x2387af82 -n 3`:
```
start;
{
    "auth_token": "",
    "content": [
        {
            "type": "table",
            "name": "Assets",
            "headers": ["token", "amount"],
            "rows": [
                ["BTC", 3942.32],
                ["BNB", 873.81],
                ["DNS", 91.073]
            ]
        },
        {
            "type": "table",
            "name": "Transaction history",
            "headers": ["time", "from", "to", "token", "amount"],
            "rows": [
                ["11/22/2021, 15:44PM", "0x2387af82", "0x98b238ae", "BTC", 2498.298],
                ["11/19/2021, 11:44AM", "0x2387af82", "0x2387af82", "DNS", 32.026],
                ["10/01/2021, 01:23AM", "0x2387af82", "0x2c4982a2", "BNB", 224.2396]
            ]
        }
    ],
    "errors": []
}
end;
```

On `import_account -sp car line cozy great meat pop`:
```
start;
{
    "auth_token": "7h89thugnt0234thg9epwotjw49hoe4y",
    "content": [],
    "errors": ["Seed phrase is incorrect"]
}
end;
```

# Commands

## Account

### 1. `create_account`

Creates new account.

Example:
```
create_account

New account has been successfully created!
address: 0x2387af82
seed_phrase: red garden awesome run chocolate nice
```

### 2. `import_account`

Checks if there is account with the given `seed_phrase`, if yes: logs in, if not: shows an error.

Required arguments:
- `seed_phrase` (flags: `-sp`, `--seed-phrase`; type: `str`) - _seed phrase\*_ (consists from 6 random english words).

Examples:
```
import_account -sp red garden awesome run chocolate nice

Account has been successfully imported!
```
```
import_account -sp car line cozy great meat pop

Error: seed phrase is incorrect!
```

### 3. `my_account` _(auth required)_

Displays current account's info.

Examples:
```
my_account

address: 0x2387af82
```
```
my_account

Error: auth is required!
```

### 4. `account_info`

Displays account info by its `address`. Shown info: assets and last `number` transactions (sorted by time).

Required arguments:
- `address` (flags: `-a`, `--address`; type: `str`) - unique account's _hash address\*_.

Optional arguments:
- `number` (flags: `-n`, `--number`; type: `int`; default: `10`) - number of transactions to show.

Examples:
```
account_info -a 0x2387af82 -n 3

ASSETS
token   amount
BTC     3942.32
BNB     873.81
DNS     91.073

TRANSACTION HISTORY
time                    from            to              token   amount
11/22/2021, 15:44PM     0x2387af82      0x98b238ae      BTC     2498.298
11/19/2021, 11:44AM     0x2387af82      0x2387af82      DNS     32.026
10/01/2021, 01:23AM     0x2387af82      0x2c4982a2      BNB     224.2396
```
```
account_info -a 0x0666acab

Error: address in incorrect!
```

## Token

### 1. `add_token` _(auth and admin rights required)_

Adds new tokens with the specified `tag` and `quantity` to _address\*_ of the user who executed the command.

Required arguments:
- `tag` (flags: `-t`, `--tag`; type: `str`) - unique token tag.
- `quantity` (flags: `-q`, `--quantity`; type: `float`) - quantity of tokens to add.

Examples:
```
add_token -t DNS -q 666

You've recieved 666 DNS tokens!
```
```
add_token -t LOL -q 2970247240

Error: admin rights are required!
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

### 3. `sell` _(auth required)_

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

Examples:
```
add_pair -t1 BTC -t2 DOGE

BTC_DOGE pair has been successfully added!
```
```
add_pair -t1 BTC -t2 DOGE

Errr: pair already exsists!
```

### 2. `delete_pair` _(auth and admin rights required)_

Deletes trading pair with the given label from the list of the avaliable pairs.

Required arguments:
- `label` (flags: `-l`, `--label`; type: `str`) - label of the pair.

Examples:
```
delete_pair -l BTC_DOGE

BTC_DOGE pair has been successfully removed!
```
```
pair_info -l BTC_LOL

Eror: pair label is incorrect!
```

### 3. `list_pairs`

Displays the list of the available trading pairs.

Optional arguments:
- `filter_by_label` (flags: `-f`, `--filter`; type: `str`) - string to filter by.

Examples:
```
list_pairs -f BTC

label
BTC_DOGE
BTC_BNB
DNS_BTC
```
```
list_pairs

No pairs found!
```

### 4. `pair_info`

Displays current buy and sell orders.

Required arguments:
- `label` (flags: `-l`, `--label`; type: `str`) - label of the pair.

Optional arguments:
- `number` (flags: `-n`, `--number`; type: `int`; default: `5`) - number of each buy/sell orders to show.


Examples:
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
```
pair_info -l BTC_LOL

Eror: pair label is incorrect!
```

## Transaction

### 1. `list_transactions`

Displays recent `number` transactions from all _addresses\*_ (sorted by time).

Optional arguments:
- `number` (flags: `-n`, `--number`; type: `int`; default: `10`) - number of transactions to show.

Examples:
```
list_transactions -n 3

time                    from            to              token   amount
11/23/2021, 12:48PM     0x2387af82      0x98b238ae      BTC     2498.298
11/23/2021, 12:48PM     0x2c4982a2      0x2387af82      DNS     32.026
11/23/2021, 12:47PM     0x98b238ae      0x2c4982a2      BNB     224.2396
```
```
list_transactions

No transactions found!
```

## Mining

### 1. `mine` _(auth required)_

Adds DNS tokens to the account, who first guessed current _mining number\*_.

Required arguments:
- `number` (flags: `-n`, `--number`; type: `int`) - possible number to guess.

Examples:
```
mine -n 7

Unsuccessful mining!
```
```
mine -n 9

You've received 3.3487 DNS tokens!
```
