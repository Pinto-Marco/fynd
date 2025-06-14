from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from . import viator_client
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import models as info_models
from. import serializers as info_serializers




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



class FynderBasicTypeView(APIView):
    permissions_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Fynder Basic Fynder Types",
        description="Get the Fynder basic Fynder Types",
        responses={200: dict}
    )
    def get(self, request):
        fynder_basic_types = info_models.FynderBasicType.objects.all()
        serializer = info_serializers.FynderBasicTypeSerializer(fynder_basic_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)