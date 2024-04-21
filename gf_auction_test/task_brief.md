# THOUGHT MACHINE Programming Test - Auction House

## Requirements

- Please complete the following programming exercise. Allow for about 4-6 hours.
- You must use either Python or Go to complete this exercise. You may use the standard library for
  your language freely, but not other third-party libraries. In your test code you may use common
  third-party test packages (e.g. pytest or testify).
- Please produce production-quality code, providing tests and comments where necessary.
- Provide all source code, ideally in a zip file / tarball so that it can be checked out and built.
  Please do not share or upload the code anywhere else (e.g. Github).
- Ensure your solution takes a user-supplied path to the input file as a command line argument.
- Provide a brief README file with instructions on how to build/run your program (and tests if
  present) - and any assumptions made.

Consider you are running an auction website in which people can put items up for sale, and others
can bid to buy them. A bid is considered valid if it:

- Arrives after the auction start time and before or on the closing time.
- Is larger than any previous valid bids submitted by the same user.

At the end of each auction, the winner will be the bidder with the highest valid bid that meets or
exceeds the reserve price, but the price paid will be the value of the second highest valid bid, or
the reserve price, whichever is higher. If there is only a single valid bid, they will pay the
reserve price of the auction. If there are no valid bids meeting or exceeding the reserve price then
the item remains unsold.

## Exercise

Given an input file containing instructions to both start auctions and place bids, you must execute
all instructions, and output for each item (upon the auction closing) the winning bid, the final
price to be paid, and the user who has won the item, as well as some basic stats about the auction.
You will be provided a basic sample input file to help you test your program.

### Input

You will receive a pipe-delimited input file representing the started auctions and bids. The first
entry on each line of this file will be a timestamp, and the file will be strictly in order of
timestamp. There are three types of rows found in this file:

#### 1. Users listing items for sale

These will appear in the format:

```text
timestamp|user_id|action|item|reserve_price|closing_time
```

- `timestamp` is an integer representing a Unix-epoch time and is the auction start time;
- `user_id` is an integer user ID;
- `action` is the string "SELL";
- `item` is a unique string code for that item;
- `reserve_price` is a decimal representing the item reserve price in the site's local currency;
- `closing_time` is an integer representing a Unix-epoch time.

#### 2. Bids on items

These will appear in the format:

```text
timestamp|user_id|action|item|bid_amount
```

- `timestamp` is an integer representing a Unix-epoch time and is the time of the bid;
- `user_id` is an integer user ID;
- `action` is the string "BID";
- `item` is a unique string code for that item;
- `bid_amount` is a decimal representing a bid in the auction site's local currency.

#### 3. Heartbeat messages

These messages may appear periodically in the input to ensure that auctions can be closed in the
absence of bids. They take the format:

```text
timestamp
```

- `timestamp` is an integer representing a Unix epoch time.

### Expected Output

The program should produce the following expected output, with each line representing the outcome of
a completed auction. This should be written to stdout and be pipe delimited with the following
format:

```text
closing_time|item|user_id|status|price_paid|total_bid_count|highest_bid|lowest_bid
```

- `closing_time` should be the Unix-epoch time when the auction finished;
- `item` should be the unique string item code;
- `user_id` should be the integer ID of the winning user, or blank if the item did not sell;
- `status` should be either "SOLD" or "UNSOLD", depending on the auction outcome;
- `price_paid` should be the price paid by the auction winner (0.00 if the item is UNSOLD), as a
  number to two decimal places;
- `total_bid_count` should be the number of valid bids received for the item;
- `highest_bid` should be the highest bid received for the item as a number to two decimal places;
- `lowest_bid` should be the lowest bid placed on the item as a number to two decimal places.

## Example

Input:

```text
10|1|SELL|toaster_1|10.00|20
12|8|BID|toaster_1|7.50
13|5|BID|toaster_1|12.50
15|8|SELL|tv_1|250.00|20
16
17|8|BID|toaster_1|20.00
18|1|BID|tv_1|150.00
19|3|BID|tv_1|200.00
20
21|3|BID|tv_1|300.00
```

Output:

```text
20|toaster_1|8|SOLD|12.50|3|20.00|7.50
20|tv_1||UNSOLD|0.00|2|200.00|150.00
```
