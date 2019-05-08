from liqpay.liqpay3 import LiqPay


def get_liqpay_data_and_signature(**params):
    liqpay = LiqPay('i73939640788', 'sDZoL85Uw9EctHamJmQohprwTNsT8yon8u1nakai')
    params = {
        'action': 'pay',
        'amount': params.get('amount'),
        'currency': params.get('currency', 'UAH'),
        'description': params.get('description', None),
        'order_id': params.get('order_id'),
        'version': '3',
        'sandbox': 1,  # sandbox mode, set to 1 to enable it
        'server_url': params.get('server_url'),  # url to callback view
    }

    data = {
        'signature': liqpay.cnb_signature(params),
        'data': liqpay.cnb_data(params)
    }

    return data

