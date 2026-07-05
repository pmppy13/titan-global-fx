from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'usd_balance', 'btc_balance', 'eth_balance', 'usdt_balance',
        'can_withdraw', 'is_staff', 'date_joined'
    )
    
    list_filter = ('can_withdraw', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('username', 'email'),
                ('first_name', 'last_name'),
                ('phone', 'country'),
            )
        }),
        
        ('Permissions', {
            'fields': (
                ('is_active', 'is_staff', 'is_superuser'),
                'groups',
                'user_permissions',
            )
        }),
        
        ('Important Dates', {
            'fields': (
                ('last_login', 'date_joined'),
                'created_at',
                'updated_at',
            )
        }),
        
        # ============================================================
        # BALANCES
        # ============================================================
        ('💰 Balances', {
            'fields': (
                ('usd_balance', 'btc_balance'),
                ('eth_balance', 'usdt_balance'),
            ),
            'classes': ('wide',),
        }),
        
        # ============================================================
        # TRADING STATS
        # ============================================================
        ('📊 Trading Statistics', {
            'fields': (
                ('total_pnl', 'win_rate'),
                ('total_trades', 'roi'),
                'trade_progress',
            ),
            'classes': ('wide',),
        }),
        
        # ============================================================
        # SIGNAL STATS
        # ============================================================
        ('📶 Signal Strength', {
            'fields': (
                'signal_strength',
                ('signal_direction', 'signal_direction_class'),
                ('signal_risk', 'signal_timeframe'),
                'signal_active_bars',
            ),
            'classes': ('wide',),
        }),
        
        # ============================================================
        # WITHDRAWAL CONTROLS
        # ============================================================
        ('🔒 Withdrawal Controls', {
            'fields': (
                'can_withdraw',
                'withdraw_disable_reason',
                'unlock_code',
            ),
            'classes': ('wide',),
        }),
        
        # ============================================================
        # SECURITY
        # ============================================================
        ('Security', {
            'fields': (
                'security_pin',
                'email_verified',
                'kyc_status',
                'referral_code',
            ),
            'classes': ('collapse',),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                ('username', 'email'),
                ('password1', 'password2'),
                ('first_name', 'last_name'),
                ('phone', 'country'),
            )
        }),
        ('Balances', {
            'fields': (
                ('usd_balance', 'btc_balance'),
                ('eth_balance', 'usdt_balance'),
            ),
        }),
        ('Trading Stats', {
            'fields': (
                ('total_pnl', 'win_rate'),
                ('total_trades', 'roi'),
                'trade_progress',
            ),
        }),
        ('Signal Stats', {
            'fields': (
                'signal_strength',
                ('signal_direction', 'signal_direction_class'),
                ('signal_risk', 'signal_timeframe'),
                'signal_active_bars',
            ),
        }),
        ('Withdrawal Controls', {
            'fields': (
                'can_withdraw',
                'withdraw_disable_reason',
                'unlock_code',
            ),
        }),
    )

admin.site.register(User, CustomUserAdmin)
