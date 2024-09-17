# encoding: utf-8 # TODO: Remove these
# KiPa(KisaPalvelu), tuloslaskentajärjestelmä partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi

from django.urls import re_path
from .models import *
from .views import *
from django.conf import settings
from django.conf.urls.static import static

tal=r"(?P<talletettu>(talletettu)?)/?$"

urlpatterns = [
        re_path(r'^apua/', apua),
        re_path(r'^$', etusivu),
        re_path(r'^post_txt/(?P<parametrit>[^/]+)/$', post_txt),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tallenna/$', tallennaKisa),
        re_path(r'^login/$', loginSivu),
        re_path(r'^logout/$', logoutSivu),
        re_path(r'^lisaaKisa/$', korvaaKisa),
        re_path(r'^(?P<kisa_nimi>[^/]+)/$', kisa),
        re_path(r'^uusiKisa/maarita/$', maaritaKisa),
        re_path(r'^(?P<kisa_nimi>[^/]+)/korvaa/$', korvaaKisa),
        re_path(r'^(?P<kisa_nimi>[^/]+)/poista/$', poistaKisa),
        re_path(r'^(?P<kisa_nimi>[^/]+)/maarita/'+tal, maaritaKisa),
        re_path(r'^(?P<kisa_nimi>[^/]+)/maarita/tehtava/$', maaritaValitseTehtava),
        re_path(r'^(?P<kisa_nimi>[^/]+)/maarita/tehtava/uusi/sarja/(?P<sarja_id>\d+)/$', maaritaTehtava),
        re_path(r'^(?P<kisa_nimi>[^/]+)/maarita/tehtava/(?P<tehtava_id>\d+)/'+tal , maaritaTehtava),
        re_path(r'^(?P<kisa_nimi>[^/]+)/maarita/vaiheet/(?P<tehtava_id>\d+)/(?P<vartio_id>\d*)/?' , tehtavanVaiheet),
        re_path(r'^(?P<kisa_nimi>[^/]+)/maarita/vartiot/'+tal, maaritaVartiot),
        re_path(r'^(?P<kisa_nimi>[^/]+)/maarita/tehtava/kopioi/sarjaan/(?P<sarja_id>\d+)/$', kopioiTehtavia),
        re_path(r'^(?P<kisa_nimi>[^/]+)/maarita/testitulos/'+tal, testiTulos),
        re_path(r'^(?P<kisa_nimi>[^/]+)/luo/sarja/(?P<sarja_id>\d+)/testitulokset/$', luoTestiTulokset),
        re_path(r'^(?P<kisa_nimi>[^/]+)/maarita/tuomarineuvos/'+tal ,tuomarineuvos),
        re_path(r'^(?P<kisa_nimi>[^/]+)/syota/(?P<tarkistus>(tarkistus/)?)$', syotaKisa),
        re_path(r'^(?P<kisa_nimi>[^/]+)/syota/(?P<tarkistus>(tarkistus/)?)tehtava/(?P<tehtava_id>\d+)/'+tal, syotaTehtava),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tulosta/normaali/$', tulosta),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tulosta/normaali/sarja/(?P<sarja_id>\d+)/$', tulostaSarja),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tulosta/tilanne/$', laskennanTilanne),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tulosta/heijasta/sarja/(?P<sarja_id>\d+)/$', heijasta),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tulosta/heijasta/$', heijasta),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tulosta/tuloste/sarja/(?P<sarja_id>\d+)/$', tulostaSarjaHTML),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tulosta/tuloste/$', tulosta),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tulosta/csv/sarja/(?P<sarja_id>\d+)/$', sarjanTuloksetCSV),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tulosta/csv/$', tulosta),
        re_path(r'^(?P<kisa_nimi>[^/]+)/tulosta/piirit/$', piirit),
]

if settings.DEBUG:
        urlpatterns += static('kipamedia/', document_root=settings.STATIC_DOC_ROOT)

