from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static


from root import settings

urlpatterns = [
    path('', lambda request: redirect('apps/')),
    path('admin/', admin.site.urls),
    path('apps/', include('apps.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
