import base64
import json
import subprocess
from subprocess import PIPE

from django.contrib.auth import get_user_model
from django.core.cache import cache

from catalog.models import Product
from .models import Order, OrderUser, OrderDelivery, OrderItemPhoto, OrderSellerComment, OrderStatusHistoryItem
from top_market_platform.celery import app
from users.models import Company, MyStore

User = get_user_model()


@app.task
def checkout_orders():
    for user in User.objects.all():
        if (Company.objects.filter(user=user).exists()
                and MyStore.objects.filter(user=user).exists()):
            token = cache.get('user_id_{}'.format(user.pk))
            if not token:
                if user.rozetka_username and user.rozetka_password:
                    curl_get_access_key = 'curl -X POST https://api.seller.rozetka.com.ua/sites ' \
                                   '-H \'Content-Type: application/json\' ' \
                                   '-H \'cache-control: no-cache\' ' \
                                   '-d \'{{\"username\": \"{username}\", \"password\": \"{password}\"}}\'' \
                        .format(username=user.rozetka_username,
                                password=base64.b64encode(bytes(user.rozetka_password, 'utf-8')).decode('utf-8'))

                    output = subprocess.check_output(curl_get_access_key, stderr=PIPE, shell=True)
                    data = json.loads(output)

                    if data['success']:
                        token = data['content']['access_token']
                        cache.set('user_id_{}'.format(user.pk), token, 60 * 60 * 24)
            if token:
                curl_get_orders_key = 'curl -X GET https://api.seller.rozetka.com.ua/orders/search' \
                                      '?expand=user,delivery,order_status_history ' \
                                      '-H \'Authorization: Bearer {token}\' ' \
                                      '-H \'cache-control: no-cache\'' \
                    .format(token=token)
                output = subprocess.check_output(curl_get_orders_key, stderr=PIPE, shell=True)
                data = json.loads(output)

                orders = data['content']['orders']
                for order in orders:
                    seller_comment_created = order.pop('seller_comment_created')
                    order_instance, created = Order.objects.update_or_create(
                        id=order['id'],
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

                    OrderUser.objects.update_or_create(
                        order=order_instance,
                        defaults=order['user']
                    )

                    delivery_dict = order['delivery']
                    city = delivery_dict['city']['name']
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
