from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = [
        path('kipa/',  include('tupa.urls')),
        path('', RedirectView.as_view(url='/kipa/', permanent=False)),
        path('admin/', admin.site.urls),
]

if settings.SERVE_MEDIA:
        urlpatterns += static('kipamedia/', document_root=settings.STATIC_DOC_ROOT)

handler500 = 'tupa.views.raportti_500'
