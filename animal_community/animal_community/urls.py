from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import show_error_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('chat_category/', include('chat_category.urls')),
]

handler404 = show_error_page

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)