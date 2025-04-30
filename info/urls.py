from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'accommodations', views.AccommodationViewSet, basename='accommodation')

urlpatterns = [
    path('', include(router.urls)),
    path('viator/v2/products/tags/', views.ViatorProductsTagsView.as_view(), name='viator-products-tags'),
    path('viator/v2/destinations/', views.ViatorDestinationsView.as_view(), name='viator-destinations'),
    path('viator/v2/search/freetext/', views.ViatorFreeTextSearchView.as_view(), name='viator-free-text-search'),
    path('viator/v2/locations/bulk/', views.ViatorLocationsBulkView.as_view(), name='viator-locations-bulk'),
    path('viator/v2/exchange-rates/', views.ViatorExchangeRatesView.as_view(), name='viator-exchange-rates'),
    path('viator/v2/products/search/', views.ViatorProductSearchView.as_view(), name='viator-product-search'),
    path('viator/v2/product/<str:product_code>', views.ViatorProductCodeView.as_view(), name='viator-product-code'),
    path('viator/v2/availability/schedules/<str:product_code>/', views.ViatorAvailabilitySchedulesView.as_view(), name='viator-availability-schedules'),
    path('viator/v2/attraction/search/', views.ViatorAttractionSearchView.as_view(), name='viator-attraction-search'),
    path('viator/v2/attraction/<str:attraction_id>/', views.ViatorAttractionIdView.as_view(), name='viator-attraction-detail'),
    # implementare le destination
    #
    #
]