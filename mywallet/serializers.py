from datetime import datetime
from mywallet.models import Transactions, Wallet
from rest_framework import serializers

class WalletSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField()
    owned_by = serializers.CharField(source='customer.user.username')
    status = serializers.SerializerMethodField()
    enabled_at = serializers.SerializerMethodField()
    balance = serializers.IntegerField()

    class Meta:
        fields=(
            "id",
            "owned_by",
            "status",
            "enabled_at",
            "balance"
        )
        model=Wallet
    
    def get_status(self, obj):
        return "enabled" if obj.is_active else "disabled"
    
    def get_enabled_at(self, obj):
        try:
            return obj.modified_at.strftime("%Y-%m-%dT%H:%M:%S%z")
        except:
            return None

class TransactionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    status = serializers.CharField()
    transacted_at = serializers.SerializerMethodField()
    type = serializers.CharField(source="transaction_type")
    amount = serializers.IntegerField()
    reference_id = serializers.UUIDField(source="wallet.id")

    class Meta:
        fields=(
            "id",
            "type",
            "status",
            "transacted_at",
            "amount",
            "reference_id"
        )
        model = Transactions
    
    def get_transacted_at(self, obj):
        try:
            return obj.modified_at.strftime("%Y-%m-%dT%H:%M:%S%z")
        except Exception:
            return None
