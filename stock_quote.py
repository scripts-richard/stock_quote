#!/usr/bin/python3
# -------------------------------------------------------------------------------
# stock_quote.py
# v2.0
# by Richard Mills
# Fetches select stock prices, compare and save differences, emails changes
# -------------------------------------------------------------------------------

from yahoo_finance import Share
import csv
import time
import locale

import gmail_helper

save_file = 'stock_quote.csv'
emails_file = 'emails.txt'


def get_existing_info():
    # Requires an existing file with the following info for eachs stock
    # ticker -- quantity -- previous price -- previous value
    stocks = []
    with open(save_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            stocks.append(row)
    return stocks


def get_changes(stocks):
    # Get current stock info and calculate changes
    changes = []
    updated_stocks = []
    for stock in stocks:
        current_price = Share(stock[0]).get_price()
        current_value = int(stock[1]) * float(current_price)
        percent_change = (float(current_price) - float(stock[2])) / float(stock[2]) # noqa
        percent_change = round(percent_change, 2)

        changes.append([stock[0], percent_change, current_value])
        updated_stocks.append([stock[0], stock[1], current_price, current_value]) # noqa
    return changes, updated_stocks


def write_changes(stocks):
    # Overwrite existing info with new info
    with open(save_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(stocks)
    return


def format_text(changes):
    # Prepare plain text and html
    current_time = time.strftime('%Y-%m-%d')

    text = current_time + '\n\n'
    change_html = ''

    locale.setlocale(locale.LC_NUMERIC, 'en_CA.UTF-8')

    for change in changes:
        dollar_view = locale.format('%.2f', change[2], True)
        text += change[0] + '  ' + str(change[1]) + '%  $' + dollar_view + '\n'
        if change[1] > 0:
            color = 'green'
        else:
            color = 'red'
        change_html += '<tr><td>%s</td>' % change[0]
        change_html += '<td class="aright %s">%s%%</td>' % (color, change[1])
        change_html += '<td class="aright">$%s</td></tr>' % dollar_view

    html = """\
    <html>
        <head>
            <style>
                td {padding: 0.5em}
                .aright {text-align: right}
                .green {color: green}
                .red {color: red}
            </style>
        </head>
        <body>
            <p>%s</p>
            <br>
            <table>
                <tr><th>Ticker</th><th>Change</th><th>Value</th></tr>
                %s
            </table>
        </body>
    </html>
    """ % (current_time, change_html)
    return text, html


def main():
    stocks = get_existing_info()
    changes, stocks = get_changes(stocks)
    write_changes(stocks)
    text, html = format_text(changes)
    sender, to = gmail_helper.get_emails(emails_file)
    gmail_helper.email(sender, to, 'Stock Quotes', text, html)


if __name__ == "__main__":
    main()
