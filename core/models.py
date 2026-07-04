from django.db import models
from django.utils.text import slugify

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question

class DepositOption(models.Model):
    METHOD_CHOICES = [
        ('bank', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
        ('paypal', 'PayPal'),
    ]

    name = models.CharField(max_length=100)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class WithdrawOption(models.Model):
    METHOD_CHOICES = [
        ('bank', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
        ('paypal', 'PayPal'),
    ]

    name = models.CharField(max_length=100)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2, default=50)
    max_amount = models.DecimalField(max_digits=20, decimal_places=2, default=100000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TermsAndConditions(models.Model):
    content = models.TextField()
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Terms v{self.version}"

# ===== WALLET ADDRESS MODEL =====
class WalletAddress(models.Model):
    """Admin-managed wallet addresses for deposit methods"""
    METHOD_CHOICES = [
        ('bank', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
        ('paypal', 'PayPal'),
    ]
    
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, unique=True)
    address = models.TextField(help_text="Wallet address, account number, or email")
    instructions = models.TextField(blank=True, help_text="Instructions shown to user")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_method_display()} - {self.address[:20]}..."

    class Meta:
        verbose_name_plural = "Wallet Addresses"
