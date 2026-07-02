from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'usd_balance', 'can_withdraw', 'date_joined']
    list_filter = ['can_withdraw', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Account Info', {'fields': ('phone', 'country', 'security_pin')}),
        ('Balances', {'fields': ('usd_balance', 'btc_balance', 'eth_balance', 'usdt_balance')}),
        ('Withdrawal Controls', {'fields': ('can_withdraw', 'withdraw_disabled_at', 'withdraw_disable_reason', 'unlock_code')}),
    )

admin.site.register(User, CustomUserAdmin)