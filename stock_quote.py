#!/usr/bin/env python3
#-----------------------------------------------------------------------------------
# stock_quote.py
<<<<<<< HEAD
# v1.0
=======
# v2.0
>>>>>>> gmail_helper
# by Richard Mills
# Fetches select stock prices, compare and save differences, emails changes
#-----------------------------------------------------------------------------------

from yahoo_finance import Share
<<<<<<< HEAD
import smtplib
import csv
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import locale

def email(toAddresses, subject, text, html):
    username = ######### EMAIL TO USE #########
    password = ######## PASSWORD ########

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = ', '.join(toAddresses)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(username, toAddresses, msg.as_string())
    server.quit()
    return

toAddress = [###### Email List #######]

# ticker -- quantity -- previous price -- previous value
stocks = []
save_file = './stock_quote.csv'
with open(save_file, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        stocks.append(row)

changes = []

for stock in stocks:
    currentPrice = Share(stock[0]).get_price()
    currentValue = int(stock[1]) * float(currentPrice)
    percentChange = (float(currentPrice) - float(stock[2])) / float(stock[2])
    percentChange = round(percentChange, 2)
    stock[2] = currentPrice
    stock[3] = currentValue
    changes.append([stock[0], percentChange, currentValue])

with open(save_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(stocks)

time = time.strftime("%Y-%m-%d")

text = "%s\n\n" %time
changeText = ""

locale.setlocale(locale.LC_NUMERIC, 'English')

for change in changes:
    dollarView = locale.format('%.2f', change[2], True)
    text += change[0] + "    " + str(change[1]) + "%    $" + dollarView + "\n"
    if change[1] > 0.0:
        color = 'green'
    else:
        color = 'red'
    changeText += '<tr><td>%s</td>' %change[0]
    changeText += '<td class="aright %s">%s%%</td>' %(color, change[1])
    changeText += '<td class="aright">$%s</td></tr>' %dollarView

stockHTML = """\
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
""" %(time, changeText)

email(toAddress, "Stocks", text, stockHTML)
=======
import csv
import time
import locale

import gmail_helper

save_file = './stock_quote.csv'

def get_existing_info():
    # Requires an existing file with the following info for eachs stock
    # ticker -- quantity -- previous price -- previous value
    stocks = []
    with open(save_file, newline = '') as f:
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
        percent_change = (float(current_price) - float(stock[2])) / float(stock[2])
        percent_change = round(percent_change, 2)

        changes.append([stock[0], percent_change, current_value])
        updated_stocks.append([stock[0], stock[1], current_price, current_value])
    return changes, updated_stocks

def write_changes(stocks):
    # Overwrite existing info with new info
    with open(save_file, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerows(stocks)
    return

def get_emails():
    # Get info from files
    # TODO: Move function to gmail_helper and hand filename
    with open('emails.txt') as f:
        emails = f.read().splitlines()
    for line in emails:
        if line[0] == '#':
            emails.remove(line)
    sender = emails.pop(0)
    return sender, emails

def format_text(changes):
    # Prepare plain text and html
    time = time.strfttime('%Y-%m-%d')

    text = time + '\n\n'
    change_html = ''

    locale.setlocale(locale.LC_NUMERIC, 'English')

    for change in changes:
        dollar_view = locale.format('%.2f', change[2], True)
        text += change[0] + '     ' + str(change[1]) + '%     $' + dollar_view + '\n'
        if change[1] > 0:
            color = 'green'
        else:
            color = 'red'
        change_html += '<tr><td>%s</td>' %change[0]
        change_html += '<td class="aright %s">%s%%</td>' %(color, change[1])
        change_html += '<td class="aright">$%s</td></tr>' %dollar_view

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
    """ %(time, change_html)
    return text, html

def main():
    stocks = get_existing_info()
    changes, stocks = get_changes(stocks)
    write_changes(stocks)
    sender, to = get_emails()
    text, html = format_text(changes)
    gmail_helper.email(sender, to, 'Stock Quotes', text, html)

main()
>>>>>>> gmail_helper
