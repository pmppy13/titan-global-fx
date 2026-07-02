from django.contrib import admin
from .models import SiteSetting, TermsAndConditions, DepositOption, WithdrawOption

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'created_at', 'updated_at']
    search_fields = ['key']

@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ['version', 'is_active', 'created_at']
    list_filter = ['is_active']

@admin.register(DepositOption)
class DepositOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'method', 'is_active', 'created_at']
    list_filter = ['method', 'is_active']

@admin.register(WithdrawOption)
class WithdrawOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'method', 'is_active', 'min_amount', 'max_amount']
    list_filter = ['method', 'is_active']