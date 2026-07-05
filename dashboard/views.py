from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseForbidden
from transactions.models import Transaction
from core.models import DepositOption, WithdrawOption

@login_required
def dashboard_index(request):
    """User dashboard view - all values default to 0 until admin changes them"""
    user = request.user
    
    # Get recent transactions
    recent_transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:10]
    
    # Calculate totals
    total_deposits = Transaction.objects.filter(
        user=user, 
        transaction_type='deposit', 
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_withdrawals = Transaction.objects.filter(
        user=user, 
        transaction_type='withdraw', 
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Get pending transactions count
    pending_transactions = Transaction.objects.filter(
        user=user, 
        status='pending'
    ).count()
    
    # ============================================================
    # TRADING STATS - Default to 0 until admin changes them
    # ============================================================
    context = {
        'user': user,
        'recent_transactions': recent_transactions,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'pending_transactions': pending_transactions,
        
        # Trading Stats (default 0)
        'total_pnl': getattr(user, 'total_pnl', 0),
        'win_rate': getattr(user, 'win_rate', 0),
        'total_trades': getattr(user, 'total_trades', 0),
        'roi': getattr(user, 'roi', 0),
        'trade_progress': getattr(user, 'trade_progress', 0),
        
        # Signal Stats (default 0)
        'signal_strength': getattr(user, 'signal_strength', 0),
        'signal_direction': getattr(user, 'signal_direction', '➡️ Neutral'),
        'signal_direction_class': getattr(user, 'signal_direction_class', 'neutral'),
        'signal_risk': getattr(user, 'signal_risk', '⚪ None'),
        'signal_timeframe': getattr(user, 'signal_timeframe', '--'),
        'signal_active_bars': getattr(user, 'signal_active_bars', 0),
    }
    
    return render(request, 'dashboard/index.html', context)


@login_required
def deposit_view(request):
    """Deposit page"""
    user = request.user
    deposit_options = DepositOption.objects.filter(is_active=True)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        method_name = request.POST.get('method_name')
        reference = request.POST.get('reference')
        notes = request.POST.get('notes')
        proof_image = request.FILES.get('proof_image')
        
        # Validation
        if not amount or not method or not method_name:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('transactions:deposit')
        
        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, 'Amount must be greater than 0.')
                return redirect('transactions:deposit')
        except ValueError:
            messages.error(request, 'Invalid amount.')
            return redirect('transactions:deposit')
        
        # Create transaction
        transaction = Transaction.objects.create(
            user=user,
            transaction_type='deposit',
            amount=amount,
            currency='USD',
            method=method,
            method_name=method_name,
            reference=reference or '',
            notes=notes or '',
            proof_image=proof_image,
            status='pending'
        )
        
        messages.success(request, f'Deposit request submitted! Reference: #{transaction.id}')
        return redirect('transactions:list')
    
    context = {
        'deposit_options': deposit_options,
    }
    return render(request, 'dashboard/deposit.html', context)


@login_required
def withdraw_view(request):
    """Withdrawal page"""
    user = request.user
    
    # Check if withdrawals are enabled
    if not user.can_withdraw:
        messages.error(request, 'Withdrawals are currently disabled for your account. Please contact support.')
        return redirect('dashboard:index')
    
    withdraw_options = WithdrawOption.objects.filter(is_active=True)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        method_name = request.POST.get('method_name')
        notes = request.POST.get('notes')
        
        # Validation
        if not amount or not method or not method_name:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('transactions:withdraw')
        
        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, 'Amount must be greater than 0.')
                return redirect('transactions:withdraw')
            
            # Check minimum withdrawal (can be set in admin)
            min_withdraw = 50  # Default, can be made dynamic from settings
            if amount < min_withdraw:
                messages.error(request, f'Minimum withdrawal amount is ${min_withdraw}.')
                return redirect('transactions:withdraw')
            
            # Check balance
            if amount > user.usd_balance:
                messages.error(request, 'Insufficient balance.')
                return redirect('transactions:withdraw')
                
        except ValueError:
            messages.error(request, 'Invalid amount.')
            return redirect('transactions:withdraw')
        
        # Create transaction
        transaction = Transaction.objects.create(
            user=user,
            transaction_type='withdraw',
            amount=amount,
            currency='USD',
            method=method,
            method_name=method_name,
            notes=notes or '',
            status='pending'
        )
        
        messages.success(request, f'Withdrawal request submitted! Reference: #{transaction.id}')
        return redirect('transactions:list')
    
    context = {
        'withdraw_options': withdraw_options,
        'user_balance': user.usd_balance,
    }
    return render(request, 'dashboard/withdraw.html', context)


@login_required
def transactions_list(request):
    """Transaction history page"""
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')
    
    # Filter by type
    tx_type = request.GET.get('type')
    if tx_type:
        transactions = transactions.filter(transaction_type=tx_type)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        transactions = transactions.filter(status=status)
    
    context = {
        'transactions': transactions,
        'tx_type': tx_type,
        'status': status,
    }
    return render(request, 'dashboard/transactions_list.html', context)


@login_required
def transaction_detail(request, transaction_id):
    """View single transaction detail"""
    user = request.user
    transaction = get_object_or_404(Transaction, id=transaction_id, user=user)
    
    context = {
        'transaction': transaction,
    }
    return render(request, 'dashboard/transaction_detail.html', context)
