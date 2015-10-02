#!/usr/bin/env python2

from bs4 import BeautifulSoup as bs
import requests
import time

cookies = {'ALIPAYJSESSIONID': ''}
url = 'https://lab.alipay.com/consume/record/items.htm'
api = ''
key = '0'


def getPaymentID(soup):
    PaymentID = []
    for i in soup.select('.consumeBizNo'):
        PaymentID.append(i.string[13:-8])
    return PaymentID


def getTime(soup):
    Time = []
    for i in soup.select('.time'):
        Time.append(int(time.mktime(time.strptime(i.string, '%Y-%m-%d %H:%M:%S'))))
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
        'PaymentIDntid': PaymentID,
        'Time': Time,
        'Name': Name,
        'Amount': Amount
    }
    requests.post(api, data=data)

if __name__ == '__main__':
    posted = []
    while True:
        if len(posted) > 1000:
            posted = []
        html = requests.get(url, cookies=cookies).text
        soup = bs(html, 'lxml')
        for i in soup.select('.amount.outlay'):
            i.parent.decompose()
        for i in soup.select('.subTransCodeValue'):
            i.decompose()
        PaymentID = getPaymentID(soup)
        Time = getTime(soup)
        Name = getName(soup)
        Amount = getAmount(soup)
        # for x, y, z, k in PaymentID, Time, Name, Amount:
        #     if x not in posted:
        #         postData(x, y, z, k)
        #         posted.append(x)
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
                print '%s\t%s\t%s\t%s' % (PaymentID[i], Time[i], Name[i].split('-')[1], Amount[i],)
                posted.append(PaymentID[i])
        time.sleep(5)
