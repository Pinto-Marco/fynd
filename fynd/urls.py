"""
URL configuration for fynd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

from fynder import views as fynder_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # google and apple login or register
    path('accounts/', include('allauth.urls')),
    path('api/dj-rest-auth/google/', fynder_views.GoogleLogin.as_view(), name='google_login'),
    path('api/dj-rest-auth/apple/', fynder_views.AppleLogin.as_view(), name='apple-login'),
    # fynder app urls
    path('api/fynder/', include('fynder.urls')),
    path('api/info/', include('info.urls')),
    path('api/fynder/trip/', include('trip.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
