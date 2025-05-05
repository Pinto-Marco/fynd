from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .booking_client import BookingAPIClient
from .models import BookingSearch, SavedAccommodation
from .serializers import BookingSearchSerializer, SavedAccommodationSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from . import viator_client
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class AccommodationViewSet(viewsets.ViewSet):
    booking_client = BookingAPIClient()

    @extend_schema(
        summary="Search Accommodations",
        description="Search for accommodations using Booking.com API with advanced filters",
        request=BookingSearchSerializer,
        responses={200: dict},
        examples=[
            OpenApiExample(
                'Example Request',
                value={
                    "checkin": "2024-03-01",
                    "checkout": "2024-03-05",
                    "adults": 2,
                    "rooms": 1,
                    "city_id": -2140479,
                    "children": [5, 8],
                    "currency": "EUR",
                    "min_price": 100,
                    "max_price": 500,
                    "meal_plan": "breakfast_included",
                    "cancellation_type": "free_cancellation",
                    "min_review_score": 8,
                    "stars": [4, 5],
                    "sort_by": "review_score",
                    "sort_direction": "descending"
                }
            )
        ]
    )
    def create(self, request):
        serializer = BookingSearchSerializer(data=request.data)
        if serializer.is_valid():
            search = serializer.save(fynder=request.user)
            
            # Convert model data to API parameters
            api_params = {
                'checkin': str(search.checkin),
                'checkout': str(search.checkout),
                'adults': search.adults,
                'rooms': search.rooms,
                'city_id': search.city_id,
            }

            # Add optional parameters if they exist
            optional_params = [
                'country', 'district', 'region', 'airport', 'children',
                'guest_allocation', 'accommodation_types', 'accommodation_facilities',
                'room_facilities', 'brands', 'currency', 'min_price', 'max_price',
                'payment_type', 'credit_card_required', 'meal_plan',
                'cancellation_type', 'min_review_score', 'stars',
                'twenty_four_hour_reception', 'travel_proud', 'sort_by',
                'sort_direction'
            ]

            for param in optional_params:
                value = getattr(search, param)
                if value is not None:
                    api_params[param] = value
            
            results = self.booking_client.search_accommodations(**api_params)
            
            return Response(results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Save Accommodation",
        description="Save an accommodation for later reference",
        request=SavedAccommodationSerializer,
        responses={201: SavedAccommodationSerializer},
        examples=[
            OpenApiExample(
                'Example Request',
                value={
                    "booking_id": 123456,
                    "search": 1,
                    "name": "Hotel Example",
                    "price": "150.00",
                    "currency": "EUR",
                    "deep_link_url": "https://booking.com/hotel/example"
                }
            )
        ]
    )
    @action(detail=False, methods=['post'])
    def save_accommodation(self, request):
        serializer = SavedAccommodationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(fynder=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Get Accommodation Details",
        description="Get detailed information about a specific accommodation",
        parameters=[
            OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH)
        ],
        responses={200: dict}
    )
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        try:
            results = self.booking_client.get_accommodation_details(int(pk))
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class ViatorProductCodeView(APIView):
    permissions_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get Viator Product Code",
        description="Get the Viator product code",
        responses={200: dict}
    )
    def get(self, request, product_code = None):
        try:
            results = viator_client.fetch_viator_product_code(product_code)
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ViatorAvailabilitySchedulesView(APIView):
    permissions_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Viator Availability Schedules",
        description="Get the Viator availability schedules",
        responses={200: dict}
    )
    def get(self, request, product_code = None):
        try:
            results = viator_client.fetch_viator_availability_schedules(product_code)
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ViatorProductsTagsView(APIView):
    permissions_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Viator Products Tags",
        description="Get the Viator products tags",
        responses={200: dict}
    )
    def get(self, request, product_code = None):
        try:
            results = viator_client.fetch_viator_products_tags()
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ViatorDestinationsView(APIView):
    permissions_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Viator Destinations",
        description="Get the Viator destinations",
        responses={200: dict}
    )
    def get(self, request, product_code = None):
        try:
            results = viator_client.fetch_viator_destinations()
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ViatorFreeTextSearchView(APIView):
    permissions_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Viator Free Text Search",
        description="Get the Viator free text",
        responses={200: dict}
    )
    def post(self, request):
        try:
            body = request.data
            results = viator_client.fetch_viator_free_text_search(body)
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ViatorLocationsBulkView(APIView):
    permissions_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Viator Locations Bulk",
        description="Get the Viator locations bulk",
        responses={200: dict}
    )
    def post(self, request):
        try:
            body = request.data
            results = viator_client.fetch_viator_locations_bulk(body)
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ViatorExchangeRatesView(APIView):
    permissions_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Viator Exchange Rates",
        description="Get the Viator exchange rates",
        responses={200: dict}
    )
    def post(self, request):
        try:
            body = request.data
            results = viator_client.fetch_viator_exchange_rates(body)
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ViatorProductSearchView(APIView):
    permissions_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Viator Products Search",
        description="Get the Viator products search for a specific accommodation",
        responses={200: dict}
    )
    def post(self, request, product_code = None):
        try:
            body = request.data
            results = viator_client.fetch_viator_products_search(body)
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ViatorAttractionIdView(APIView):
    permissions_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Viator Attraction Id",
        description="Get the Viator attraction id for a specific attraction",
        responses={200: dict}
    )
    def get(self, request, attraction_id = None):
        try:
            results = viator_client.fetch_viator_attractions_id(attraction_id)
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ViatorAttractionSearchView(APIView):
    permissions_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Viator Attraction Search",
        description="Get the Viator attraction search for a specific attraction",
        responses={200: dict}
    )
    def post(self, request):
        try:
            body = request.data
            results = viator_client.fetch_viator_attractions_search(body)
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )