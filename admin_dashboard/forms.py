from django import forms
from core.models import DepositOption, WithdrawOption, TermsAndConditions

class DepositOptionForm(forms.ModelForm):
    class Meta:
        model = DepositOption
        fields = ['name', 'method', 'description', 'instructions', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'method': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class WithdrawOptionForm(forms.ModelForm):
    class Meta:
        model = WithdrawOption
        fields = ['name', 'method', 'description', 'instructions', 'is_active', 'min_amount', 'max_amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'method': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'min_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
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

class DisableWithdrawForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=True)
    generate_code = forms.BooleanField(required=False, initial=True, label='Generate unlock code for user')
