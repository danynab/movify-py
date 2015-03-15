__author__ = 'mvidalgarcia'

import json

import requests


def bitcoin_payment(price, order_number, return_url):
    # Payment Request
    print('Payment Request')

    values = {
        'settled_currency': "BTC",
        'return_url': return_url,
        'price': price,
        'currency': "EUR",
        'reference': {
            'customer_name': "Movify",
            'order_number': order_number,
            'customer_email': "movify@movify.com"
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token fmzGW06lF3hQAqPZyAY8dymz'
    }

    url = 'https://private-anon-2b8feed1a-bitcoinpaycom.apiary-proxy.com/api/v1/payment/btc'
    values = json.dumps(values, ensure_ascii=False)
    response = requests.post(url, data=values, headers=headers)
    if response.status_code == 200:
        payment_id = response.json()['data']['payment_id']
        payment_url = response.json()['data']['payment_url']

        print('Payment URL:', payment_url)
        return {'id': payment_id, 'url': payment_url}


def bitcoin_payment_check(payment_id):
    headers = {
        'Authorization': 'Token fmzGW06lF3hQAqPZyAY8dymz'
    }

    url = 'https://private-anon-2b8feed1a-bitcoinpaycom.apiary-proxy.com/api/v1/payment/btc/' + payment_id
    response = requests.get(url, headers=headers)
    print(response.text)
    if response.status_code == 200:
        payment_status = response.json()['data']['status']
        return payment_status