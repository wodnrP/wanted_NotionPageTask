from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include



router = DefaultRouter()


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
