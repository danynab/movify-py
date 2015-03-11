import paypalrestsdk

__author__ = 'mvidalgarcia'


def paypal_payment(price, quantity, name, description, sku, return_url, cancel_url):
    paypalrestsdk.configure({
        'mode': "sandbox",
        'client_id': "AQkquBDf1zctJOWGKWUEtKXm6qVhueUEMvXO_-MCI4DQQ4-LWvkDLIN2fGsd",
        'client_secret': "EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX"
    })

    payment = paypalrestsdk.Payment({
        'intent': "sale",
        'payer': {
            'payment_method': "paypal"
        },
        'redirect_urls': {
            'return_url': return_url,
            'cancel_url': cancel_url
        },
        'transactions':
            [
                {
                    'amount': {
                        'total': price,
                        'currency': "EUR"
                    },
                    'description': description,
                    'item_list': {
                        'items':
                            [
                                {
                                    'quantity': quantity,
                                    'name': name,
                                    'price': price,
                                    'sku': sku,
                                    'currency': "EUR"
                                }
                            ]
                    }
                }
            ]
    })

    payment.create()
    approval_url = [link['href'] for link in payment['links'] if link['rel'] == 'approval_url'][0]
    return {'id': payment.id, 'url': approval_url}