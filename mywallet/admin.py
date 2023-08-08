from django.contrib import admin
from .models import Customer, Wallet, Transactions

# Register the Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_xid', 'user', 'created_at', 'modified_at')
    readonly_fields = ('created_at', 'modified_at')

# Register the Wallet model
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'is_active', 'balance', 'created_at', 'modified_at')
    readonly_fields = ('created_at', 'modified_at')

# Register the Transactions model
@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'status', 'transaction_type', 'created_at', 'modified_at')
    readonly_fields = ('created_at', 'modified_at')
