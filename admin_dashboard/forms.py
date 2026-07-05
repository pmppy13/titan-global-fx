from django import forms
from django.contrib.auth import get_user_model
from core.models import DepositOption, WithdrawOption, TermsAndConditions

User = get_user_model()

class DepositOptionForm(forms.ModelForm):
    class Meta:
        model = DepositOption
        fields = '__all__'

class WithdrawOptionForm(forms.ModelForm):
    class Meta:
        model = WithdrawOption
        fields = '__all__'

class TermsForm(forms.ModelForm):
    class Meta:
        model = TermsAndConditions
        fields = '__all__'

class DisableWithdrawForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True,
        label='Reason for disabling withdrawals'
    )
    generate_code = forms.BooleanField(
        required=False,
        label='Generate unlock code'
    )

class BalanceUpdateForm(forms.Form):
    ACTION_CHOICES = [
        ('add', 'Add to Balance'),
        ('subtract', 'Subtract from Balance'),
        ('set', 'Set Balance To'),
    ]
    CURRENCY_CHOICES = [
        ('usd_balance', 'USD'),
        ('btc_balance', 'BTC'),
        ('eth_balance', 'ETH'),
        ('usdt_balance', 'USDT'),
    ]
    action = forms.ChoiceField(choices=ACTION_CHOICES)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
    amount = forms.DecimalField(max_digits=20, decimal_places=8, min_value=0)
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False
    )

class TradingStatsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'total_pnl', 'win_rate', 'total_trades', 'roi', 'trade_progress',
            'signal_strength', 'signal_direction', 'signal_direction_class',
            'signal_risk', 'signal_timeframe', 'signal_active_bars',
        ]
