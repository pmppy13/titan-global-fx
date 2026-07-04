from django import forms
from .models import Transaction

class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'method', 'method_name', 'reference', 'proof_image', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '1',
                'placeholder': 'Enter amount in USD',
                'style': 'width:100%;padding:12px 16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;color:#ffffff;font-size:0.95rem;transition:all 0.4s ease;outline:none;'
            }),
            'method': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width:100%;padding:12px 16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;color:#ffffff;font-size:0.95rem;transition:all 0.4s ease;outline:none;'
            }),
            'method_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Bank Transfer, BTC, PayPal',
                'style': 'width:100%;padding:12px 16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;color:#ffffff;font-size:0.95rem;transition:all 0.4s ease;outline:none;'
            }),
            'reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter transaction reference number',
                'style': 'width:100%;padding:12px 16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;color:#ffffff;font-size:0.95rem;transition:all 0.4s ease;outline:none;'
            }),
            'proof_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'style': 'width:100%;padding:10px 12px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;color:#ffffff;font-size:0.95rem;transition:all 0.4s ease;outline:none;'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...',
                'style': 'width:100%;padding:12px 16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;color:#ffffff;font-size:0.95rem;transition:all 0.4s ease;outline:none;resize:vertical;min-height:80px;font-family:inherit;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders for method field choices
        self.fields['method'].choices = [
            ('', '-- Select Payment Method --'),
            ('bank', '🏦 Bank Transfer'),
            ('crypto', '₿ Cryptocurrency'),
            ('paypal', '💳 PayPal'),
        ]


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'method', 'method_name', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '1',
                'placeholder': 'Enter amount in USD',
                'style': 'width:100%;padding:12px 16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;color:#ffffff;font-size:0.95rem;transition:all 0.4s ease;outline:none;'
            }),
            'method': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width:100%;padding:12px 16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;color:#ffffff;font-size:0.95rem;transition:all 0.4s ease;outline:none;'
            }),
            'method_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Bank Transfer, BTC, PayPal',
                'style': 'width:100%;padding:12px 16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;color:#ffffff;font-size:0.95rem;transition:all 0.4s ease;outline:none;'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...',
                'style': 'width:100%;padding:12px 16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;color:#ffffff;font-size:0.95rem;transition:all 0.4s ease;outline:none;resize:vertical;min-height:80px;font-family:inherit;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['method'].choices = [
            ('', '-- Select Withdrawal Method --'),
            ('bank', '🏦 Bank Transfer'),
            ('crypto', '₿ Cryptocurrency'),
            ('paypal', '💳 PayPal'),
        ]

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError('Amount must be greater than 0.')
        return amount
