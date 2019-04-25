import json
import subprocess
import time
from subprocess import PIPE
from django.contrib.auth import get_user_model

from catalog.models import Product
from catalog.utils import get_rozetka_auth_token
from .constants import OrderStatusGroups
from .models import Order, OrderUser, OrderDelivery, OrderItemPhoto, OrderSellerComment, OrderStatusHistoryItem
from top_market_platform.celery import app
from users.models import Company, MyStore

User = get_user_model()


def upload_orders(user, token_rozetka, extra_query=''):
    next_page = 1
    processing = True
    while processing:
        curl_get_orders_key = 'curl -X GET \'https://api.seller.rozetka.com.ua/orders/search' \
                              '?expand=user,delivery,order_status_history&page={page}{extra_query}\' ' \
                              '-H \'Authorization: Bearer {token_rozetka}\' ' \
                              '-H \'cache-control: no-cache\'' \
            .format(token_rozetka=token_rozetka, page=next_page, extra_query=extra_query)
        output = subprocess.check_output(curl_get_orders_key, stderr=PIPE, shell=True)
        data = json.loads(output)

        orders = data['content']['orders']

        if next_page == data['content']['_meta']['pageCount']:
            processing = False
        else:
            next_page += 1

        for order in orders:
            seller_comment_created = order.pop('seller_comment_created')
            order_instance, created = Order.objects.update_or_create(
                id=order['id'],
                user=user,
                defaults={
                    'market_id': order['market_id'],
                    'created': order['created'],
                    'amount': order['amount'],
                    'amount_with_discount': order['amount_with_discount'],
                    'cost': order['cost'],
                    'cost_with_discount': order['cost_with_discount'],
                    'status': order['status'],
                    'status_group': order['status_group'],
                    'current_seller_comment': order['current_seller_comment'],
                    'comment': order['comment'],
                    'user_phone': order['user_phone'],
                    'from_warehouse': order['from_warehouse'],
                    'ttn': order['ttn'],
                    'total_quantity': order['total_quantity'],
                    'can_copy': order['can_copy'],
                    'created_type': order['created_type']
                }
            )
            if seller_comment_created:
                order_instance.seller_comment_created = seller_comment_created
            order_instance.save()

            user_id = order['user'].pop('id')
            OrderUser.objects.update_or_create(
                order=order_instance,
                rozetka_id=user_id,
                defaults=order['user']
            )

            delivery_dict = order['delivery']
            city = delivery_dict['city']['name'] if 'city' in delivery_dict.keys() and delivery_dict['city'] else None
            delivery_dict.pop('city')
            OrderDelivery.objects.update_or_create(
                order=order_instance,
                city=city,
                defaults=order['delivery']
            )

            for photo_dict in order['items_photos']:
                OrderItemPhoto.objects.update_or_create(
                    order=order_instance,
                    product_id=photo_dict['id'],
                    url=photo_dict['url']
                )
                if Product.objects.filter(id=photo_dict['id']).exists():
                    order_instance.product.add(photo_dict['id'])

            for seller_comment_dict in order['seller_comment']:
                OrderSellerComment.objects.update_or_create(
                    order=order_instance,
                    comment=seller_comment_dict['comment'],
                    created=seller_comment_dict['created']
                )

            for order_status_history_dict in order['order_status_history']:
                OrderStatusHistoryItem.objects.update_or_create(
                    order=order_instance,
                    status_id=order_status_history_dict['status_id'],
                    created=order_status_history_dict['created']
                )


@app.task
def checkout_orders():
    for user in User.objects.filter(role='PARTNER'):
        if (Company.objects.filter(user=user).exists()
                and MyStore.objects.filter(user=user).exists()):
            token_rozetka = get_rozetka_auth_token(user)
            if token_rozetka:
                if not user.rozetka_old_orders_imported:
                    for order_type in dict(OrderStatusGroups.STATUS_GROUPS).keys():
                        extra_query = '&type={}'.format(order_type)
                        upload_orders(user, token_rozetka, extra_query=extra_query)
                        time.sleep(0.3)
                    user.rozetka_old_orders_imported = True
                    user.save()
                else:
                    upload_orders(user, token_rozetka)
