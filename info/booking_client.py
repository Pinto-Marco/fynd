import os
import requests
from datetime import datetime
from typing import Dict, List, Optional

class BookingAPIClient:
    def __init__(self):
        self.base_url = os.getenv('BOOKING_API_URL')
        self.api_key = os.getenv('BOOKING_API_KEY')
        self.affiliate_id = os.getenv('BOOKING_AFFILIATE_ID')
        
    def _get_headers(self) -> Dict:
        return {
            'Authorization': f'Bearer {self.api_key}',
            'X-Affiliate-Id': self.affiliate_id,
            'Content-Type': 'application/json'
        }
    
    def search_accommodations(self, **params) -> Dict:
        url = f"{self.base_url}/accommodations/search"
        
        payload = {
            "booker": {
                "country": params.get('country', 'it'),
                "platform": "desktop"
            },
            "checkin": str(params['checkin']),
            "checkout": str(params['checkout']),
            "guests": {
                "number_of_adults": params['adults'],
                "number_of_rooms": params['rooms'],
            },
            "extras": [
                "extra_charges",
                "products",
                "photos",  # Add photos to extras
                "property_highlight_strip"
            ]
        }

        # Location parameters
        if params.get('city_id'):
            payload['city'] = params['city_id']
        if params.get('district'):
            payload['district'] = params['district']
        if params.get('region'):
            payload['region'] = params['region']
        if params.get('airport'):
            payload['airport'] = params['airport']

        # Guest details
        if params.get('children'):
            payload['guests']['children'] = params['children']
        if params.get('guest_allocation'):
            payload['guests']['allocation'] = params['guest_allocation']

        # Accommodation filters
        if params.get('accommodation_types'):
            payload['accommodation_types'] = params['accommodation_types']
        if params.get('accommodation_facilities'):
            payload['accommodation_facilities'] = params['accommodation_facilities']
        if params.get('room_facilities'):
            payload['room_facilities'] = params['room_facilities']
        if params.get('brands'):
            payload['brands'] = params['brands']

        # Price and payment
        if params.get('currency'):
            payload['currency'] = params['currency']
        if params.get('min_price') or params.get('max_price'):
            payload['price'] = {}
            if params.get('min_price'):
                payload['price']['minimum'] = float(params['min_price'])
            if params.get('max_price'):
                payload['price']['maximum'] = float(params['max_price'])
        if params.get('payment_type'):
            payload['payment'] = {'timing': params['payment_type']}
        if params.get('credit_card_required'):
            if 'payment' not in payload:
                payload['payment'] = {}
            payload['payment']['credit_card_required'] = params['credit_card_required']

        # Meal and cancellation
        if params.get('meal_plan'):
            payload['meal_plan'] = params['meal_plan']
        if params.get('cancellation_type'):
            payload['cancellation_type'] = params['cancellation_type']

        # Additional filters
        if params.get('min_review_score') or params.get('stars'):
            payload['rating'] = {}
            if params.get('min_review_score'):
                payload['rating']['minimum_review_score'] = params['min_review_score']
            if params.get('stars'):
                payload['rating']['stars'] = params['stars']
        if params.get('twenty_four_hour_reception'):
            payload['24_hour_reception'] = params['twenty_four_hour_reception']
        if params.get('travel_proud'):
            payload['travel_proud'] = params['travel_proud']

        # Sorting
        if params.get('sort_by') and params.get('sort_direction'):
            payload['sort'] = {
                'by': params['sort_by'],
                'direction': params['sort_direction']
            }

        response = requests.post(url, headers=self._get_headers(), json=payload)
        return response.json()
    
    def get_accommodation_details(self, accommodation_id: int) -> Dict:
        url = f"{self.base_url}/accommodations/details"
        payload = {
            "accommodation_id": accommodation_id,
            "extras": [
                "description",
                "policies",
                "facilities",
                "photos",  # Add photos to extras
                "room_photos"
            ]
        }
        response = requests.post(url, headers=self._get_headers(), json=payload)
        return response.json()


# curl --request POST 'https://demandapi-sandbox.booking.com/3.1/accommodations/search' \
# --header 'X-Affiliate-Id: 123456'\
# --header 'Authorization: Bearer xyz.........xyz'\