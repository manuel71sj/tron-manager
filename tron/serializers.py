from rest_framework import serializers


class TronCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    symbol = serializers.CharField(required=True, max_length=10)


class TronMintSerializer(serializers.Serializer):
    owner_address = serializers.CharField(required=True, max_length=34, min_length=34)
    owner_private_key = serializers.CharField(
        required=True, max_length=64, min_length=64
    )

    contract_address = serializers.CharField(
        required=True, max_length=34, min_length=34
    )
    to_address = serializers.CharField(required=True, max_length=34, min_length=34)
    token_uri = serializers.CharField(required=True)
    token_id = serializers.IntegerField(required=False)
