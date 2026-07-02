from django.db import models

class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

class TermsAndConditions(models.Model):
    content = models.TextField()
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Terms v{self.version}"

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
    min_amount = models.DecimalField(max_digits=20, decimal_places=2, default=50)
    max_amount = models.DecimalField(max_digits=20, decimal_places=2, default=100000)
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