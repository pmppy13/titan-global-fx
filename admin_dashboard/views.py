from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
import secrets
import string

from core.models import DepositOption, WithdrawOption, TermsAndConditions
from transactions.models import Transaction
from .forms import DepositOptionForm, WithdrawOptionForm, TermsForm, DisableWithdrawForm, BalanceForm

User = get_user_model()

# ===== FIXED: Admin Required Decorator =====
def admin_required(view_func):
    """
    Decorator that requires the user to be logged in AND be a superuser/staff.
    """
    def wrapped(request, *args, **kwargs):
        # First check if user is logged in
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access the admin dashboard.')
            return redirect('accounts:login')
        
        # Then check if user is admin (superuser or staff)
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'You do not have permission to access the admin dashboard.')
            return redirect('dashboard:index')
        
        return view_func(request, *args, **kwargs)
    return wrapped

# ========== DASHBOARD OVERVIEW ==========
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

# ========== USER MANAGEMENT ==========
@admin_required
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_dashboard/users.html', {'users': users})

@admin_required
def admin_user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')
    
    form = DisableWithdrawForm()
    balance_form = BalanceForm()
    
    if request.method == 'POST':
        if 'disable_withdraw' in request.POST:
            form = DisableWithdrawForm(request.POST)
            if form.is_valid():
                reason = form.cleaned_data['reason']
                generate_code = form.cleaned_data.get('generate_code', False)
                code = None
                if generate_code:
                    code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                
                user.can_withdraw = False
                user.withdraw_disabled_at = timezone.now()
                user.withdraw_disable_reason = reason
                if code:
                    user.unlock_code = code
                user.save()
                
                messages.success(request, f'Withdrawals disabled for {user.username}. Unlock code: {code}')
                return redirect('admin_dashboard:user_detail', user_id=user_id)
        
        elif 'balance_action' in request.POST:
            balance_form = BalanceForm(request.POST)
            if balance_form.is_valid():
                action = balance_form.cleaned_data['action']
                amount = balance_form.cleaned_data['amount']
                currency = balance_form.cleaned_data.get('currency', 'usd')
                
                if currency == 'usd':
                    if action == 'add':
                        user.usd_balance += amount
                        messages.success(request, f'Added ${amount} to {user.username}\'s USD balance')
                    else:
                        if user.usd_balance >= amount:
                            user.usd_balance -= amount
                            messages.success(request, f'Removed ${amount} from {user.username}\'s USD balance')
                        else:
                            messages.error(request, f'Insufficient balance. {user.username} only has ${user.usd_balance}')
                            return redirect('admin_dashboard:user_detail', user_id=user_id)
                elif currency == 'btc':
                    if action == 'add':
                        user.btc_balance += amount
                        messages.success(request, f'Added {amount} BTC to {user.username}\'s balance')
                    else:
                        if user.btc_balance >= amount:
                            user.btc_balance -= amount
                            messages.success(request, f'Removed {amount} BTC from {user.username}\'s balance')
                        else:
                            messages.error(request, f'Insufficient balance. {user.username} only has {user.btc_balance} BTC')
                            return redirect('admin_dashboard:user_detail', user_id=user_id)
                elif currency == 'eth':
                    if action == 'add':
                        user.eth_balance += amount
                        messages.success(request, f'Added {amount} ETH to {user.username}\'s balance')
                    else:
                        if user.eth_balance >= amount:
                            user.eth_balance -= amount
                            messages.success(request, f'Removed {amount} ETH from {user.username}\'s balance')
                        else:
                            messages.error(request, f'Insufficient balance. {user.username} only has {user.eth_balance} ETH')
                            return redirect('admin_dashboard:user_detail', user_id=user_id)
                elif currency == 'usdt':
                    if action == 'add':
                        user.usdt_balance += amount
                        messages.success(request, f'Added {amount} USDT to {user.username}\'s balance')
                    else:
                        if user.usdt_balance >= amount:
                            user.usdt_balance -= amount
                            messages.success(request, f'Removed {amount} USDT from {user.username}\'s balance')
                        else:
                            messages.error(request, f'Insufficient balance. {user.username} only has {user.usdt_balance} USDT')
                            return redirect('admin_dashboard:user_detail', user_id=user_id)
                
                user.save()
                return redirect('admin_dashboard:user_detail', user_id=user_id)
    
    return render(request, 'admin_dashboard/user_detail.html', {
        'user': user,
        'transactions': transactions,
        'form': form,
        'balance_form': balance_form,
    })

@admin_required
def admin_enable_withdraw(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        code = request.POST.get('unlock_code', '').strip()
        if user.enable_withdrawals(code):
            messages.success(request, f'Withdrawals enabled for {user.username}')
        else:
            messages.error(request, 'Invalid unlock code.')
    return redirect('admin_dashboard:user_detail', user_id=user_id)

# ========== TRANSACTION MANAGEMENT ==========
@admin_required
def admin_transactions(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard/transactions.html', {'transactions': transactions})

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

# ========== DEPOSIT OPTIONS ==========
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

# ========== WITHDRAW OPTIONS ==========
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

# ========== TERMS & CONDITIONS ==========
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