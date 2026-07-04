from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.transactions.models import Transaction

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
    
    # Trading stats (can be stored in User model or separate TradingStats model)
    # For now using defaults that admin can override via admin panel
    
    context = {
        'user': user,
        'recent_transactions': recent_transactions,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'total_pnl': getattr(user, 'total_pnl', 2450),
        'win_rate': getattr(user, 'win_rate', 68),
        'total_trades': getattr(user, 'total_trades', 142),
        'roi': getattr(user, 'roi', 18.5),
        'trade_progress': getattr(user, 'trade_progress', 68),
        'signal_strength': getattr(user, 'signal_strength', 82),
        'signal_direction': getattr(user, 'signal_direction', '📈 Bullish'),
        'signal_direction_class': getattr(user, 'signal_direction_class', 'bullish'),
        'signal_risk': getattr(user, 'signal_risk', '🟡 Medium'),
        'signal_timeframe': getattr(user, 'signal_timeframe', '4H'),
        'signal_active_bars': getattr(user, 'signal_active_bars', 5),
    }
    
    return render(request, 'dashboard/index.html', context)
