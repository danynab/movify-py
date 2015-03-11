import hashlib

__author__ = 'mvidalgarcia'

commerce_data = {
    "MERCHANT_ID": "082108630",
    "ACQUIRER_BIN": "0000554002",
    "TERMINAL_ID": "00000003",
    "CLAVE_ENCRIPTACION": "87401456",
    "TIPO_MONEDA": "978",
    "EXPONENTE": "2"
}


def cajastur_payment(operation, price, url_ok, url_error):
    price = str(int(price*100))
    return {
        "operation": operation,
        "price": price,
        "commerce_data": commerce_data,
        "url_ok": url_ok,
        "url_error": url_error,
        "signature": compute_signature(operation, price, url_ok, url_error)
    }


def compute_signature(operation, price, url_ok, url_error):
    message = commerce_data["CLAVE_ENCRIPTACION"] + \
              commerce_data["MERCHANT_ID"] + \
              commerce_data["ACQUIRER_BIN"] + \
              commerce_data["TERMINAL_ID"] + \
              operation + \
              price + \
              commerce_data["TIPO_MONEDA"] + \
              commerce_data["EXPONENTE"] + \
              "" + \
              "SHA1" + \
              url_ok + \
              url_error
    my_sha = hashlib.sha1()
    my_sha.update(str.encode(message))
    digest = my_sha.digest()
    return ''.join('{:02x}'.format(x) for x in digest)