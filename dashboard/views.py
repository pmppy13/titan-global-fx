from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from transactions.models import Transaction

@login_required
def dashboard_index(request):
    user = request.user
    recent_transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:10]
    
    total_deposits = Transaction.objects.filter(
        user=user, 
        transaction_type='deposit', 
        status='completed'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    total_withdrawals = Transaction.objects.filter(
        user=user, 
        transaction_type='withdraw', 
        status='completed'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    context = {
        'user': user,
        'usd_balance': user.usd_balance,
        'btc_balance': user.btc_balance,
        'eth_balance': user.eth_balance,
        'usdt_balance': user.usdt_balance,
        'recent_transactions': recent_transactions,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
    }
    return render(request, 'dashboard/index.html', context)