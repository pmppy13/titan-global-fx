from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Core app (home, about, contact, login, signup)
    path('', include('core.urls')),
    
    # Authentication (if using accounts app)
    path('accounts/', include('accounts.urls')),
    
    # Dashboard (if using dashboard app)
    path('dashboard/', include('dashboard.urls')),
    
    # Transactions (if using transactions app)
    path('transactions/', include('transactions.urls')),
    
    # Admin Dashboard (if using admin_dashboard app)
    path('admin-dashboard/', include('admin_dashboard.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
