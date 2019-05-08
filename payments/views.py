from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from liqpay.liqpay3 import LiqPay

from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import permissions, status, generics, viewsets
from django.contrib.auth import get_user_model
from marketplace.models import PocketPlan
from payments.constants import TransactionTypes, TransactionSources
from payments.models import PaymentTransaction
from payments.serializers import PocketIdSerializer, PaymentTransactionSerializer
from payments.utils import get_liqpay_data_and_signature

User = get_user_model()


class LiqPayPocketBuyView(APIView):
    """
    method: POST,
    body:
        pocket_id - ID пакета (1 - базовый, 2 - полный)
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = PocketIdSerializer

    def post(self, request, *args, **kwargs):
        pocket = get_object_or_404(PocketPlan, id=request.data.get('pocket_id'))
        transaction = PaymentTransaction.objects.last()
        params = {
            'amount': str(pocket.price),
            'currency': pocket.currency,
            'description': 'Payment for clothes',
            'order_id': "{}_{}_{}".format(request.user.id, pocket.id, transaction.id + 2 if transaction else 1),
            'server_url': 'https://3f4fd68e.ngrok.io/api/v1/payments/pay-callback/', # url to callback view
        }

        response_data = get_liqpay_data_and_signature(**params)

        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )


class LiqPayPocketCallBackView(APIView):

    def post(self, request, *args, **kwargs):
        liqpay = LiqPay('i73939640788', 'sDZoL85Uw9EctHamJmQohprwTNsT8yon8u1nakai')
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign('i73939640788' + data + 'sDZoL85Uw9EctHamJmQohprwTNsT8yon8u1nakai')

        response = liqpay.decode_data_from_str(data)
        if sign == signature:
            response['is_valid_signature'] = True
        user = User.objects.get(id=int(response['order_id'].split('_')[0]))
        PaymentTransaction.objects.create(
            user=user,
            amount=response.get('amount_credit'),
            trans_type=TransactionTypes.LIQPAY,
            status=response.get('status', None),
            err_description=response.get('err_description', None),
            is_valid_signature=response.get('is_valid_signature', False)
        )
        if response.get('status') == 'success':
            user.user_pocket_id = int(response['order_id'].split('_')[1])
            user.save()
        return HttpResponse()


class PaymentTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentTransactionSerializer

    http_method_names = ['get', ]

    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)
