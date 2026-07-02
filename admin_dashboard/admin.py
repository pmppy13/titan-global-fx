from django.contrib import admin
from .models import AdminActionLog

@admin.register(AdminActionLog)
class AdminActionLogAdmin(admin.ModelAdmin):
    list_display = ['admin', 'action', 'created_at']
    list_filter = ['created_at']
    search_fields = ['admin__username', 'action']
    readonly_fields = ['created_at']