from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from PerevalApp.views import PerevalViewset
from .yasg import urlpatterns as doc_urls

router = routers.DefaultRouter()
router.register(r'submitData', PerevalViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
urlpatterns += doc_urls