from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from transactions.models import Transaction

@login_required
def dashboard_index(request):
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
    
    # Get trading stats from user model (admin controlled)
    context = {
        'user': user,
        'recent_transactions': recent_transactions,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'total_pnl': user.total_pnl,
        'win_rate': user.win_rate,
        'total_trades': user.total_trades,
        'roi': user.roi,
        'trade_progress': user.trade_progress,
        'signal_strength': user.signal_strength,
        'signal_direction': user.signal_direction,
        'signal_direction_class': user.signal_direction_class,
        'signal_risk': user.signal_risk,
        'signal_timeframe': user.signal_timeframe,
        'signal_active_bars': user.signal_active_bars,
    }
    
    return render(request, 'dashboard/index.html', context)
