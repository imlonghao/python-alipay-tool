#!/usr/bin/env python2

from __future__ import print_function
from bs4 import BeautifulSoup as bs
import requests
import time

cookies = {'ALIPAYJSESSIONID': ''}
url = 'https://lab.alipay.com/consume/record/items.htm'
api = ''
key = ''


def getPaymentID(soup):
    PaymentID = []
    for i in soup.select('.consumeBizNo'):
        PaymentID.append(i.string.strip())
    return PaymentID


def getTime(soup):
    Time = []
    timeFormat = '%Y-%m-%d %H:%M:%S'
    for i in soup.select('.time'):
        Time.append(int(time.mktime(time.strptime(i.string, timeFormat))))
    return Time


def getName(soup):
    Name = []
    for i in soup.select('.emoji-li'):
        for ii in i.stripped_strings:
            Name.append(ii)
    return Name


def getAmount(soup):
    Amount = []
    for i in soup.select('.amount.income'):
        Amount.append(i.string)
    return Amount


def postData(PaymentID, Time, Name, Amount):
    data = {
        'key': key,
        'ddh': PaymentID,
        'time': Time,
        'name': Name,
        'money': Amount
    }
    requests.post(api, data=data)

if __name__ == '__main__':
    posted = []
    while True:
        if len(posted) > 1000:
            posted = []
        req = requests.get(url, cookies=cookies)
        if req.url.startswith('https://auth.alipay.com/'):
            print('Authentication failed!')
            import sys
            sys.exit(0)
        html = req.text
        soup = bs(html, 'lxml')
        for i in soup.select('.amount.outlay'):
            i.parent.decompose()
        for i in soup.select('.subTransCodeValue'):
            i.decompose()
        PaymentID = getPaymentID(soup)
        Time = getTime(soup)
        Name = getName(soup)
        Amount = getAmount(soup)
        length = len(PaymentID)
        for i in range(length):
            if not Name[i].startswith(u'\u4ed8\u6b3e-'):
                continue
            if PaymentID[i] not in posted:
                postData(
                        PaymentID[i],
                        Time[i],
                        Name[i].split('-')[1],
                        Amount[i],
                    )
                posted.append(PaymentID[i])
        time.sleep(5)
