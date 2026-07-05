from django import forms
from core.models import DepositOption, WithdrawOption, TermsAndConditions

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
