from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'accommodations', views.AccommodationViewSet, basename='accommodation')

urlpatterns = [
    path('', include(router.urls)),
    path('viator/v2/product/<str:product_code>', views.ViatorProductCodeView.as_view(), name='viator-product-code'),
    path('viator/v2/products/tags/', views.ViatorProductsTagsView.as_view(), name='viator-products-tags'),
    path('viator/v2/products/search/', views.ViatorProductSearchView.as_view(), name='viator-product-search'),
    path('viator/v2/attraction/<str:attraction_id>/', views.ViatorAttractionIdView.as_view(), name='viator-attraction-detail'),
]