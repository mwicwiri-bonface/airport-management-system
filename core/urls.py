
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('finance/', include(('finance.urls', 'finance'), namespace="finance")),
    path('', include(('passenger.urls', 'passenger'), namespace="passenger")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'passenger.errors.error_404'
handler500 = 'passenger.errors.error_500'
handler403 = 'passenger.errors.error_403'
handler400 = 'passenger.errors.error_400'
