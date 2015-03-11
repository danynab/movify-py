import paypalrestsdk

__author__ = 'mvidalgarcia'


def paypal_payment(price, quantity, name, description, sku, return_url, cancel_url):

    paypalrestsdk.configure({
      'mode': 'sandbox',
      'client_id': 'AQkquBDf1zctJOWGKWUEtKXm6qVhueUEMvXO_-MCI4DQQ4-LWvkDLIN2fGsd',
      'client_secret': 'EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX'
    })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url
        },
        "transactions":
            [
                {
                    "amount": {
                        "total": price,
                        "currency": "EUR"
                    },
                    "description": description,
                    "item_list": {
                        "items":
                            [
                                {
                                    "quantity": quantity,
                                    "name": name,
                                    "price": price,
                                    "sku": sku,
                                    "currency": "EUR"
                                }
                            ]
                    }
                }
            ]
    })

    payment.create()
    approval_url = [link["href"] for link in payment["links"] if link["rel"] == "approval_url"][0]
    # print(payment)
    # print(payment['id'])
    return approval_url

    # payment = paypalrestsdk.Payment.find("PAY-91026765784018620KT7O4SI")
    # payment.execute({"payer_id": "3ESVXSE43SHLG"})
    # print(payment)


if __name__ == "__main__":

    # Example payer (PayPal)
    # Email: movify@movify.com
    # Pass: 12345678


    # Example data
    my_price = "11.99"
    my_quantity = "1"
    my_name = "Movify One-Month Subscription"
    my_description = "This is the payment description."
    my_sku = "1monthsubs00000"  # kind of id product (stock-keeping unit)
    my_return_url = "http://www.google.com"
    my_cancel_url = "http://www.apple.com/"
    url_payment = paypal_payment(my_price, my_quantity, my_name, my_description, my_sku, my_return_url, my_cancel_url)
    print("URL PayPal Payment", url_payment)