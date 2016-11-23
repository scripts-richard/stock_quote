#!/usr/bin/env python3
#-----------------------------------------------------------------------------------
# stock_quote.py
# v1.0
# by Richard Mills
# Fetches select stock prices, compare and save differences, emails changes
#-----------------------------------------------------------------------------------

from yahoo_finance import Share
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
