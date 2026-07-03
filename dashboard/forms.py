from django import forms
from transactions.models import Transaction
from core.models import DepositOption, WithdrawOption

class DepositForm(forms.ModelForm):
    method = forms.ChoiceField(choices=[], required=True)
    method_name = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = Transaction
        fields = ['amount', 'method', 'method_name', 'reference', 'proof_image', 'notes']  # ADDED proof_image
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction reference number'}),
            'proof_image': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        deposit_options = DepositOption.objects.filter(is_active=True)
        choices = [(opt.method, opt.name) for opt in deposit_options]
        self.fields['method'].choices = [('', 'Select method...')] + choices
        self.fields['method_name'].widget = forms.HiddenInput()
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount > 0:
            return amount
        raise forms.ValidationError('Amount must be greater than 0.')

class WithdrawForm(forms.ModelForm):
    method = forms.ChoiceField(choices=[], required=True)
    method_name = forms.CharField(max_length=100, required=True)
    account_details = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 4, 
            'placeholder': 'Enter your bank account details (account name, number, bank, routing/SWIFT) OR your wallet address OR your PayPal email...'
        }),
        required=True,
        label='Your Account Details'
    )
    
    class Meta:
        model = Transaction
        fields = ['amount', 'method', 'method_name', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        withdraw_options = WithdrawOption.objects.filter(is_active=True)
        choices = [(opt.method, opt.name) for opt in withdraw_options]
        self.fields['method'].choices = [('', 'Select method...')] + choices
        self.fields['method_name'].widget = forms.HiddenInput()
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount > 0:
            return amount
        raise forms.ValidationError('Amount must be greater than 0.')
