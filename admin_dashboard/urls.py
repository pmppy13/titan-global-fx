from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='index'),
    path('users/', views.admin_users, name='users'),
    path('users/<int:user_id>/', views.admin_user_detail, name='user_detail'),
    path('users/<int:user_id>/enable-withdraw/', views.admin_enable_withdraw, name='enable_withdraw'),
    path('transactions/', views.admin_transactions, name='transactions'),
    path('transactions/<int:transaction_id>/', views.admin_transaction_detail, name='transaction_detail'),
    path('transactions/<int:transaction_id>/action/', views.admin_transaction_action, name='transaction_action'),
    path('deposit-options/', views.admin_deposit_options, name='deposit_options'),
    path('deposit-options/<int:option_id>/edit/', views.admin_edit_deposit_option, name='edit_deposit_option'),
    path('deposit-options/<int:option_id>/delete/', views.admin_delete_deposit_option, name='delete_deposit_option'),
    path('withdraw-options/', views.admin_withdraw_options, name='withdraw_options'),
    path('withdraw-options/<int:option_id>/edit/', views.admin_edit_withdraw_option, name='edit_withdraw_option'),
    path('withdraw-options/<int:option_id>/delete/', views.admin_delete_withdraw_option, name='delete_withdraw_option'),
    path('terms/', views.admin_terms, name='terms'),
    path('terms/<int:terms_id>/edit/', views.admin_edit_terms, name='edit_terms'),
    path('wallet-addresses/', views.admin_wallet_addresses, name='wallet_addresses'),
    path('wallet-addresses/<int:address_id>/edit/', views.admin_edit_wallet_address, name='edit_wallet_address'),
]
