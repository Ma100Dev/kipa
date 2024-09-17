from django.urls import re_path, include
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = re_path('',
        (r'^kipa/',  include('tupa.urls')),
        (r'^admin/', include(admin.site.urls)),
)

if settings.SERVE_MEDIA:
        urlpatterns += re_path('',
                (r'^kipamedia/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_DOC_ROOT}),)

handler500 = 'tupa.views.raportti_500'
