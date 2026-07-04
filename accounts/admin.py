from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'usd_balance', 'btc_balance', 'eth_balance', 'usdt_balance',
        'can_withdraw', 'is_staff', 'date_joined'
    )
    
    # Fields to filter by
    list_filter = ('can_withdraw', 'is_staff', 'is_active', 'date_joined')
    
    # Search fields
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Order by
    ordering = ('-date_joined',)
    
    # ============================================================
    # FIELDSETS - This is where you define what shows in the edit form
    # ============================================================
    fieldsets = (
        # Personal Info
        ('Personal Information', {
            'fields': (
                ('username', 'email'),
                ('first_name', 'last_name'),
                ('phone', 'country'),
                ('date_of_birth', 'address'),
                ('city', 'postal_code'),
            )
        }),
        
        # Permissions
        ('Permissions', {
            'fields': (
                ('is_active', 'is_staff', 'is_superuser'),
                'groups',
                'user_permissions',
            )
        }),
        
        # Important Dates
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
            'description': 'User account balances in different currencies.'
        }),
        
        # ============================================================
        # TRADING STATS (Admin controllable)
        # ============================================================
        ('📊 Trading Statistics', {
            'fields': (
                ('total_pnl', 'win_rate'),
                ('total_trades', 'roi'),
                'trade_progress',
            ),
            'classes': ('wide',),
            'description': 'Trading performance metrics that display on the user dashboard.'
        }),
        
        # ============================================================
        # SIGNAL STATS (Admin controllable)
        # ============================================================
        ('📶 Signal Strength', {
            'fields': (
                'signal_strength',
                ('signal_direction', 'signal_direction_class'),
                ('signal_risk', 'signal_timeframe'),
                'signal_active_bars',
            ),
            'classes': ('wide',),
            'description': 'Signal strength and direction displayed on the dashboard.'
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
            'description': 'Control user withdrawal permissions. Unlock code is shown to user when disabled.'
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
    
    # ============================================================
    # ADD FIELDSET - For creating new users
    # ============================================================
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

# Register the custom admin
admin.site.register(User, CustomUserAdmin)
