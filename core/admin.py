from django.contrib import admin
from .models import FAQ, DepositOption, WithdrawOption, TermsAndConditions, WalletAddress

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
    ordering = ['order']

@admin.register(DepositOption)
class DepositOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'method', 'is_active']
    list_filter = ['method', 'is_active']
    search_fields = ['name', 'description']

@admin.register(WithdrawOption)
class WithdrawOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'method', 'is_active', 'min_amount', 'max_amount']
    list_filter = ['method', 'is_active']
    search_fields = ['name', 'description']

@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ['version', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['content', 'version']

@admin.register(WalletAddress)
class WalletAddressAdmin(admin.ModelAdmin):
    list_display = ['method', 'address', 'is_active', 'created_at']
    list_filter = ['method', 'is_active']
    search_fields = ['address', 'instructions']
