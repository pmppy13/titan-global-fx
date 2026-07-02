from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdrawal'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    method = models.CharField(max_length=50)
    method_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    reference = models.CharField(max_length=100, blank=True)
    proof_image = models.ImageField(upload_to='transaction_proofs/', blank=True, null=True)
    notes = models.TextField(blank=True)
    
    # New field for user's account details (for withdrawals)
    account_details = models.TextField(blank=True, help_text="User's bank account, wallet address, or PayPal email")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.user.username} - ${self.amount}"