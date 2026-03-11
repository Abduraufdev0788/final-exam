from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/auth/", include("apps.authentication.urls")),
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/", include("apps.sellers.urls")),
    path("api/v1/", include("apps.product.urls")),
    path("api/v1/", include("apps.category.urls")),
    path("api/v1/", include("apps.favorites.urls")),
    path("api/v1/", include("apps.orders.urls")),
    path("api/v1/", include("apps.reviews.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

         
]