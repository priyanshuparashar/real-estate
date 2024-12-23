from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("Base.urls")),
    path("ex@minp@anel/", admin.site.urls ),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )