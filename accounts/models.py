from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    security_pin = models.CharField(max_length=6, blank=True)
    
    # Balance fields
    usd_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    btc_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    eth_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    usdt_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    # Withdrawal controls
    can_withdraw = models.BooleanField(default=True)
    withdraw_disabled_at = models.DateTimeField(null=True, blank=True)
    withdraw_disable_reason = models.TextField(blank=True)
    unlock_code = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    def get_total_balance_usd(self):
        return self.usd_balance
    
    def disable_withdrawals(self, reason='', code=None):
        self.can_withdraw = False
        self.withdraw_disabled_at = timezone.now()
        self.withdraw_disable_reason = reason
        if code:
            self.unlock_code = code
        self.save()
    # Add to accounts/models.py - inside User model

# Trading stats (admin controllable)
total_pnl = models.DecimalField(max_digits=20, decimal_places=2, default=2450)
win_rate = models.IntegerField(default=68)  # Percentage
total_trades = models.IntegerField(default=142)
roi = models.DecimalField(max_digits=10, decimal_places=2, default=18.5)
trade_progress = models.IntegerField(default=68)  # Percentage

# Signal stats (admin controllable)
signal_strength = models.IntegerField(default=82)  # Percentage
signal_direction = models.CharField(max_length=50, default='📈 Bullish')
signal_direction_class = models.CharField(max_length=20, default='bullish')  # bullish, bearish, neutral
signal_risk = models.CharField(max_length=50, default='🟡 Medium')
signal_timeframe = models.CharField(max_length=20, default='4H')
signal_active_bars = models.IntegerField(default=5)  # Number of active bars in meter
    def enable_withdrawals(self, code):
        if self.unlock_code and self.unlock_code == code:
            self.can_withdraw = True
            self.unlock_code = ''
            self.withdraw_disabled_at = None
            self.withdraw_disable_reason = ''
            self.save()
            return True
        return False
