from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Transaction
from core.models import DepositOption, WithdrawOption
from dashboard.forms import DepositForm, WithdrawForm

@login_required
def deposit_view(request):
    deposit_options = DepositOption.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = 'deposit'
            transaction.status = 'pending'
            transaction.save()
            messages.success(request, f'Deposit request submitted! Reference: {transaction.reference or transaction.id}')
            return redirect('dashboard:index')
    else:
        form = DepositForm()
    
    return render(request, 'dashboard/deposit.html', {
        'form': form,
        'deposit_options': deposit_options,
    })

@login_required
def withdraw_view(request):
    # ============================================================
    # 1. GET the withdrawal options and user balance (needed for both states)
    # ============================================================
    withdraw_options = WithdrawOption.objects.filter(is_active=True)
    user_balance = request.user.usd_balance

    # ============================================================
    # 2. CHECK: If withdrawals are DISABLED
    # ============================================================
    if not request.user.can_withdraw:
        
        # --- 2a. POST request: User submitted unlock code ---
        if request.method == 'POST':
            code = request.POST.get('unlock_code', '').strip()
            
            if not code:
                messages.error(request, 'Please enter an unlock code.')
                return render(request, 'dashboard/withdraw.html', {
                    'withdraw_options': withdraw_options,
                    'user_balance': user_balance,
                    'error': 'Please enter an unlock code.'
                })
            
            # Try to enable withdrawals with the code
            if request.user.enable_withdrawals(code):
                messages.success(request, 'Withdrawals have been re-enabled successfully!')
                return redirect('transactions:withdraw')
            else:
                messages.error(request, 'Invalid unlock code. Please try again.')
                return render(request, 'dashboard/withdraw.html', {
                    'withdraw_options': withdraw_options,
                    'user_balance': user_balance,
                    'error': 'Invalid unlock code. Please try again.'
                })
        
        # --- 2b. GET request: Show the disabled page with unlock form ---
        return render(request, 'dashboard/withdraw.html', {
            'withdraw_options': withdraw_options,
            'user_balance': user_balance,
        })

    # ============================================================
    # 3. Withdrawals are ENABLED - Normal flow
    # ============================================================
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            # Check if user has enough balance
            if amount > user_balance:
                messages.error(request, 'Insufficient balance for this withdrawal.')
                return render(request, 'dashboard/withdraw.html', {
                    'form': form,
                    'withdraw_options': withdraw_options,
                    'user_balance': user_balance,
                })
            
            # Create the transaction
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = 'withdraw'
            transaction.status = 'pending'
            transaction.account_details = form.cleaned_data['account_details']
            transaction.save()
            
            messages.success(request, f'Withdrawal request submitted! Reference: {transaction.id}')
            return redirect('dashboard:index')
        else:
            # Form invalid - show errors
            return render(request, 'dashboard/withdraw.html', {
                'form': form,
                'withdraw_options': withdraw_options,
                'user_balance': user_balance,
            })
    
    # ============================================================
    # 4. GET request: Show the normal withdraw page
    # ============================================================
    form = WithdrawForm()
    return render(request, 'dashboard/withdraw.html', {
        'form': form,
        'withdraw_options': withdraw_options,
        'user_balance': user_balance,
    })

@login_required
def transactions_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/transactions.html', {
        'transactions': transactions,
    })

# ===== AJAX endpoint for code verification (optional) =====
@login_required
def verify_unlock_code(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        
        if not code:
            return JsonResponse({'success': False, 'message': 'Please enter an unlock code.'})
        
        user = request.user
        
        if user.unlock_code and user.unlock_code == code:
            user.enable_withdrawals(code)
            return JsonResponse({'success': True, 'message': 'Withdrawals re-enabled successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid unlock code. Please check with support.'})
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request format.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})