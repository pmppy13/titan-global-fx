from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    # Personal Info
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Security
    security_pin = models.CharField(max_length=6, blank=True)
    email_verified = models.BooleanField(default=False)
    kyc_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('verified', 'Verified'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    referral_code = models.CharField(max_length=20, blank=True, unique=True)
    
    # ============================================================
    # BALANCES
    # ============================================================
    usd_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    btc_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    eth_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    usdt_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    # ============================================================
    # TRADING STATS (Admin controllable)
    # ============================================================
    total_pnl = models.DecimalField(
        max_digits=20, decimal_places=2, default=2450,
        help_text="Total Profit/Loss displayed on dashboard"
    )
    win_rate = models.IntegerField(
        default=68,
        help_text="Win rate percentage (0-100)"
    )
    total_trades = models.IntegerField(
        default=142,
        help_text="Total number of trades"
    )
    roi = models.DecimalField(
        max_digits=10, decimal_places=2, default=18.5,
        help_text="Return on Investment percentage"
    )
    trade_progress = models.IntegerField(
        default=68,
        help_text="Trade progress percentage (0-100)"
    )
    
    # ============================================================
    # SIGNAL STATS (Admin controllable)
    # ============================================================
    signal_strength = models.IntegerField(
        default=82,
        help_text="Signal strength percentage (0-100)"
    )
    signal_direction = models.CharField(
        max_length=50,
        default='📈 Bullish',
        help_text="Signal direction text (e.g., 📈 Bullish, 📉 Bearish, ➡️ Neutral)"
    )
    signal_direction_class = models.CharField(
        max_length=20,
        default='bullish',
        choices=[
            ('bullish', 'Bullish'),
            ('bearish', 'Bearish'),
            ('neutral', 'Neutral'),
        ],
        help_text="CSS class for direction color"
    )
    signal_risk = models.CharField(
        max_length=50,
        default='🟡 Medium',
        help_text="Risk level (e.g., 🟢 Low, 🟡 Medium, 🔴 High)"
    )
    signal_timeframe = models.CharField(
        max_length=20,
        default='4H',
        help_text="Timeframe (e.g., 1H, 4H, 1D, 1W)"
    )
    signal_active_bars = models.IntegerField(
        default=5,
        help_text="Number of active bars in the signal meter (0-10)"
    )
    
    # ============================================================
    # WITHDRAWAL CONTROLS
    # ============================================================
    can_withdraw = models.BooleanField(
        default=True,
        help_text="Uncheck to disable user withdrawals"
    )
    withdraw_disabled_at = models.DateTimeField(null=True, blank=True)
    withdraw_disable_reason = models.TextField(
        blank=True,
        help_text="Reason shown to user when withdrawals are disabled"
    )
    unlock_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Code required to re-enable withdrawals"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def disable_withdrawals(self, reason='', code=None):
        """Disable user withdrawals with reason and optional unlock code"""
        self.can_withdraw = False
        self.withdraw_disabled_at = timezone.now()
        self.withdraw_disable_reason = reason
        if code:
            self.unlock_code = code
        self.save()

    def enable_withdrawals(self, code):
        """Enable withdrawals if code matches"""
        if self.unlock_code and self.unlock_code == code:
            self.can_withdraw = True
            self.unlock_code = ''
            self.withdraw_disabled_at = None
            self.withdraw_disable_reason = ''
            self.save()
            return True
        return False

    def get_total_balance_usd(self):
        """Calculate total balance in USD"""
        # Simplified - you can add conversion logic here
        return self.usd_balance
