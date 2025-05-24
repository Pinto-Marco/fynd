from rest_framework import serializers
from .models import BookingSearch, SavedAccommodation
from . import models as info_models

class BookingSearchSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data.get('checkin') and data.get('checkout'):
            if data['checkin'] >= data['checkout']:
                raise serializers.ValidationError(
                    "Checkout date must be after checkin date"
                )
        if data.get('min_price') and data.get('max_price'):
            if data['min_price'] > data['max_price']:
                raise serializers.ValidationError(
                    "Maximum price must be greater than minimum price"
                )
        return data
    class Meta:
        model = BookingSearch
        fields = [
            'checkin', 'checkout', 'adults', 'rooms',
            'city_id', 'country', 'district', 'region', 'airport',
            'children', 'guest_allocation',
            'accommodation_types', 'accommodation_facilities',
            'room_facilities', 'brands',
            'currency', 'min_price', 'max_price',
            'payment_type', 'credit_card_required',
            'meal_plan', 'cancellation_type',
            'min_review_score', 'stars',
            'twenty_four_hour_reception', 'travel_proud',
            'sort_by', 'sort_direction'
        ]

class SavedAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedAccommodation
        fields = [
            'booking_id', 'search', 'name', 'price', 
            'currency', 'deep_link_url', 'main_photo_url', 'photos'
        ]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = info_models.Tag
        fields = ['id', 'name', 'description']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = info_models.Schedule
        fields = ['id', 'start_date', 'end_date', 'type']

class FynderBasicCardsSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=255)
    # description = serializers.CharField(max_length=255)
    tags = serializers.SerializerMethodField()
    schedules = serializers.SerializerMethodField()

    class Meta:
        model = info_models.FynderBasicCard
        fields = [ 'id', 'name', 'description', 'tags', 'schedules'] # 'img'

    def get_tags(self, obj):
        return TagSerializer(obj.get_tags(), many=True).data
        

    def get_schedules(self, obj):
        return ScheduleSerializer(obj.get_schedules(), many=True).data