# Fetch and Save Stock Information

Using the Python Yahoo Finance module, stock information is requested,
compared, emailed, and saved.

## Usage
The script expects an 'emails.txt' file to be present in the same folder.
This file contains a newline separated list of emails. The first email is the
sender and the remaining are receivers.

The 'stock_quote.csv' is expected to already exist with each line containing
the stock ticker, the quantity owned, the previous price, and the previous
value (price * quantity). 

## Note:
Emails are sent using my gmail_helper script which has been modified slightly
from the Gmail API tutorials.
