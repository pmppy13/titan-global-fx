from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),          # Just 'core.urls' if core is in root
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('transactions/', include('transactions.urls')),
    path('admin-dashboard/', include('admin_dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
