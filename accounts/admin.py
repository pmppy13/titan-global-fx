from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Trading Stats', {
            'fields': (
                'total_pnl', 'win_rate', 'total_trades', 'roi', 'trade_progress',
            )
        }),
        ('Signal Stats', {
            'fields': (
                'signal_strength', 'signal_direction', 'signal_direction_class',
                'signal_risk', 'signal_timeframe', 'signal_active_bars',
            )
        }),
        ('Balance', {
            'fields': ('usd_balance', 'btc_balance', 'eth_balance', 'usdt_balance')
        }),
        ('Withdrawal Controls', {
            'fields': ('can_withdraw', 'withdraw_disable_reason', 'unlock_code')
        }),
    )

admin.site.register(User, CustomUserAdmin)
