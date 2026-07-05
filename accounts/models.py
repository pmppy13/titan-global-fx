from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    # Personal Info
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Security
    security_pin = models.CharField(max_length=6, blank=True)
    
    # ============================================================
    # BALANCES
    # ============================================================
    usd_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    btc_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    eth_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    usdt_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
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
        return self.usd_balance
