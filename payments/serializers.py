from rest_framework import serializers

from payments.models import PaymentTransaction


class PocketIdSerializer(serializers.Serializer):
    pocket_id = serializers.IntegerField()

    class Meta:
        fields = (
            'pocket_id',
        )


class PaymentTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentTransaction
        fields = (
            'amount',
            'trans_type',
            'source',
            'status',
            'err_description',
        )
