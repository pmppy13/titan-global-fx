from django import forms
from core.models import DepositOption, WithdrawOption, TermsAndConditions

class DepositOptionForm(forms.ModelForm):
    # Bank fields
    bank_name = forms.CharField(max_length=200, required=False, label='Bank Name')
    account_name = forms.CharField(max_length=200, required=False, label='Account Name')
    account_number = forms.CharField(max_length=50, required=False, label='Account Number')
    routing_number = forms.CharField(max_length=50, required=False, label='Routing Number')
    swift_code = forms.CharField(max_length=20, required=False, label='SWIFT Code')
    
    # Crypto fields
    coin_name = forms.CharField(max_length=50, required=False, label='Coin Name (e.g., BTC, ETH)')
    wallet_address = forms.CharField(max_length=200, required=False, label='Wallet Address')
    network = forms.CharField(max_length=50, required=False, label='Network (e.g., ERC20, BEP20)')
    
    # PayPal fields
    paypal_email = forms.EmailField(required=False, label='PayPal Email')
    paypal_link = forms.URLField(required=False, label='PayPal Payment Link')
    
    class Meta:
        model = DepositOption
        fields = ['name', 'method', 'description', 'instructions', 
                  'min_amount', 'max_amount', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'method': forms.Select(attrs={'class': 'form-control', 'id': 'id_method'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'min_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.details:
            details = self.instance.details
            self.fields['bank_name'].initial = details.get('bank_name', '')
            self.fields['account_name'].initial = details.get('account_name', '')
            self.fields['account_number'].initial = details.get('account_number', '')
            self.fields['routing_number'].initial = details.get('routing_number', '')
            self.fields['swift_code'].initial = details.get('swift_code', '')
            self.fields['coin_name'].initial = details.get('coin_name', '')
            self.fields['wallet_address'].initial = details.get('wallet_address', '')
            self.fields['network'].initial = details.get('network', '')
            self.fields['paypal_email'].initial = details.get('paypal_email', '')
            self.fields['paypal_link'].initial = details.get('paypal_link', '')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        details = {}
        method = self.cleaned_data.get('method')
        if method == 'bank':
            details['bank_name'] = self.cleaned_data.get('bank_name', '')
            details['account_name'] = self.cleaned_data.get('account_name', '')
            details['account_number'] = self.cleaned_data.get('account_number', '')
            details['routing_number'] = self.cleaned_data.get('routing_number', '')
            details['swift_code'] = self.cleaned_data.get('swift_code', '')
        elif method == 'crypto':
            details['coin_name'] = self.cleaned_data.get('coin_name', '')
            details['wallet_address'] = self.cleaned_data.get('wallet_address', '')
            details['network'] = self.cleaned_data.get('network', '')
        elif method == 'paypal':
            details['paypal_email'] = self.cleaned_data.get('paypal_email', '')
            details['paypal_link'] = self.cleaned_data.get('paypal_link', '')
        instance.details = details
        if commit:
            instance.save()
        return instance

class WithdrawOptionForm(forms.ModelForm):
    class Meta:
        model = WithdrawOption
        fields = ['name', 'method', 'description', 'instructions', 
                  'min_amount', 'max_amount', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'method': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'min_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TermsForm(forms.ModelForm):
    class Meta:
        model = TermsAndConditions
        fields = ['content', 'version', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ===== DISABLE WITHDRAW FORM =====
class DisableWithdrawForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Why are you disabling withdrawals?'}), 
        required=True,
        label='Reason for Disabling'
    )
    generate_code = forms.BooleanField(
        required=False, 
        initial=True, 
        label='Generate unlock code for user',
        help_text='The user will need this code to re-enable withdrawals.'
    )

# ===== BALANCE MANAGEMENT FORM =====
class BalanceForm(forms.Form):
    ACTION_CHOICES = [
        ('add', 'Add Funds'),
        ('remove', 'Remove Funds'),
    ]
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('btc', 'BTC'),
        ('eth', 'ETH'),
        ('usdt', 'USDT'),
    ]
    
    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'})
    )
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    reason = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason for balance change (optional)'})
    )
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount > 0:
            return amount
        raise forms.ValidationError('Amount must be greater than 0.')