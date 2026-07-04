from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.http import HttpResponse
from django.core.files.storage import default_storage
import secrets
import string

# FIXED: Remove 'apps.' prefix since apps are in root
from core.models import DepositOption, WithdrawOption, TermsAndConditions, WalletAddress
from transactions.models import Transaction
from .forms import DepositOptionForm, WithdrawOptionForm, TermsForm, DisableWithdrawForm

User = get_user_model()

def admin_required(view_func):
    decorated = user_passes_test(
        lambda u: u.is_superuser or u.is_staff,
        login_url='login'
    )(view_func)
    return decorated

@admin_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_transactions = Transaction.objects.count()
    pending_transactions = Transaction.objects.filter(status='pending').count()
    total_deposits = Transaction.objects.filter(transaction_type='deposit', status='completed').aggregate(total=models.Sum('amount'))['total'] or 0

    recent_transactions = Transaction.objects.order_by('-created_at')[:10]

    context = {
        'total_users': total_users,
        'total_transactions': total_transactions,
        'pending_transactions': pending_transactions,
        'total_deposits': total_deposits,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'admin_dashboard/index.html', context)

@admin_required
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_dashboard/users.html', {'users': users})

@admin_required
def admin_user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')

    if request.method == 'POST':
        form = DisableWithdrawForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            generate_code = form.cleaned_data.get('generate_code', False)
            code = None
            if generate_code:
                code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            user.disable_withdrawals(reason, code)
            messages.success(request, f'Withdrawals disabled for {user.username}. Unlock code: {code}')
            return redirect('admin_dashboard:user_detail', user_id=user_id)
    else:
        form = DisableWithdrawForm()

    return render(request, 'admin_dashboard/user_detail.html', {
        'user': user,
        'transactions': transactions,
        'form': form,
    })

@admin_required
def admin_enable_withdraw(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        code = request.POST.get('unlock_code')
        if user.enable_withdrawals(code):
            messages.success(request, f'Withdrawals enabled for {user.username}')
        else:
            messages.error(request, 'Invalid unlock code.')
    return redirect('admin_dashboard:user_detail', user_id=user_id)

@admin_required
def admin_transactions(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard/transactions.html', {'transactions': transactions})

@admin_required
def admin_transaction_detail(request, transaction_id):
    """View transaction details including proof image"""
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'admin_dashboard/transaction_detail.html', {'transaction': transaction})

@admin_required
def admin_transaction_action(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            transaction.status = 'approved'
            transaction.processed_at = timezone.now()
            messages.success(request, f'Transaction #{transaction.id} approved')
        elif action == 'complete':
            transaction.status = 'completed'
            transaction.processed_at = timezone.now()
            # Update user balance
            if transaction.transaction_type == 'deposit':
                transaction.user.usd_balance += transaction.amount
                transaction.user.save()
            elif transaction.transaction_type == 'withdraw':
                transaction.user.usd_balance -= transaction.amount
                transaction.user.save()
            messages.success(request, f'Transaction #{transaction.id} completed and balance updated')
        elif action == 'reject':
            transaction.status = 'rejected'
            transaction.processed_at = timezone.now()
            messages.success(request, f'Transaction #{transaction.id} rejected')
        elif action == 'cancel':
            transaction.status = 'cancelled'
            messages.success(request, f'Transaction #{transaction.id} cancelled')
        transaction.save()
    return redirect('admin_dashboard:transactions')

@admin_required
def admin_deposit_options(request):
    options = DepositOption.objects.all()
    if request.method == 'POST':
        form = DepositOptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deposit option created successfully')
            return redirect('admin_dashboard:deposit_options')
    else:
        form = DepositOptionForm()
    return render(request, 'admin_dashboard/deposit_options.html', {
        'options': options,
        'form': form,
    })

@admin_required
def admin_edit_deposit_option(request, option_id):
    option = get_object_or_404(DepositOption, id=option_id)
    if request.method == 'POST':
        form = DepositOptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deposit option updated successfully')
            return redirect('admin_dashboard:deposit_options')
    else:
        form = DepositOptionForm(instance=option)
    return render(request, 'admin_dashboard/deposit_options.html', {
        'option': option,
        'form': form,
        'edit_mode': True,
    })

@admin_required
def admin_delete_deposit_option(request, option_id):
    option = get_object_or_404(DepositOption, id=option_id)
    option.delete()
    messages.success(request, 'Deposit option deleted successfully')
    return redirect('admin_dashboard:deposit_options')

@admin_required
def admin_withdraw_options(request):
    options = WithdrawOption.objects.all()
    if request.method == 'POST':
        form = WithdrawOptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Withdraw option created successfully')
            return redirect('admin_dashboard:withdraw_options')
    else:
        form = WithdrawOptionForm()
    return render(request, 'admin_dashboard/withdraw_options.html', {
        'options': options,
        'form': form,
    })

@admin_required
def admin_edit_withdraw_option(request, option_id):
    option = get_object_or_404(WithdrawOption, id=option_id)
    if request.method == 'POST':
        form = WithdrawOptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
            messages.success(request, 'Withdraw option updated successfully')
            return redirect('admin_dashboard:withdraw_options')
    else:
        form = WithdrawOptionForm(instance=option)
    return render(request, 'admin_dashboard/withdraw_options.html', {
        'option': option,
        'form': form,
        'edit_mode': True,
    })

@admin_required
def admin_delete_withdraw_option(request, option_id):
    option = get_object_or_404(WithdrawOption, id=option_id)
    option.delete()
    messages.success(request, 'Withdraw option deleted successfully')
    return redirect('admin_dashboard:withdraw_options')

@admin_required
def admin_terms(request):
    terms = TermsAndConditions.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = TermsForm(request.POST)
        if form.is_valid():
            TermsAndConditions.objects.filter(is_active=True).update(is_active=False)
            form.save()
            messages.success(request, 'Terms and conditions updated successfully')
            return redirect('admin_dashboard:terms')
    else:
        form = TermsForm()
    return render(request, 'admin_dashboard/terms.html', {
        'terms': terms,
        'form': form,
    })

@admin_required
def admin_edit_terms(request, terms_id):
    term = get_object_or_404(TermsAndConditions, id=terms_id)
    if request.method == 'POST':
        form = TermsForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            messages.success(request, 'Terms updated successfully')
            return redirect('admin_dashboard:terms')
    else:
        form = TermsForm(instance=term)
    return render(request, 'admin_dashboard/terms.html', {
        'term': term,
        'form': form,
        'edit_mode': True,
    })

@admin_required
def admin_wallet_addresses(request):
    """View and manage wallet addresses"""
    wallet_addresses = WalletAddress.objects.all()
    return render(request, 'admin_dashboard/wallet_addresses.html', {
        'wallet_addresses': wallet_addresses,
    })

@admin_required
def admin_edit_wallet_address(request, address_id):
    """Edit a wallet address"""
    wallet = get_object_or_404(WalletAddress, id=address_id)
    if request.method == 'POST':
        method = request.POST.get('method')
        address = request.POST.get('address')
        instructions = request.POST.get('instructions')
        is_active = request.POST.get('is_active') == 'on'
        
        wallet.method = method
        wallet.address = address
        wallet.instructions = instructions
        wallet.is_active = is_active
        wallet.save()
        
        messages.success(request, f'Wallet address for {wallet.get_method_display()} updated successfully')
        return redirect('admin_dashboard:wallet_addresses')
    
    return render(request, 'admin_dashboard/edit_wallet_address.html', {
        'wallet': wallet,
    })
