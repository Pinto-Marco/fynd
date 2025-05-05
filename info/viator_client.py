import requests
from django.conf import settings
from . import viator_client


def fetch_viator_product_code(productCode):
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY

    url = f"{VIATOR_API_URL}/products/{productCode}"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching activity data: {response.status_code}")
        return None

def fetch_viator_products_tags():
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/products/tags"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching activity data: {response.status_code}")
        return None


# TODO add query params to the request
def fetch_viator_products_search():
    
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/products/search"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    
    # body example
    body = {
        "filtering": { # required
            "destination": "732", # required
            # "tags": [
            # "<integer>",
            # "<integer>"
            # ],
            "flags": [ 
            "SPECIAL_OFFER",
            ],
            # "confirmationType": "<string>",
            # "rating": {
            # "from": "<integer>",
            # "to": "<integer>"
            # },
            # "durationInMinutes": {
            # "from": "<integer>",
            # "to": "<integer>"
            # },
            # "includeAutomaticTranslations": true,
            # "attractionId": "<integer>",
            # "lowestPrice": "<number>",
            # "highestPrice": "<number>",
            # "startDate": "<date>",
            # "endDate": "<date>"
        },
        "currency": "EUR",  # required
        "sorting": {
            "sort": "TRAVELER_RATING",
            "order": "DESCENDING"
        },
        "pagination": { 
            "start": 1,
            "count": 10
        }
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching activity data: {response.status_code}")
        return None


def fetch_viator_attractions_id(attractionId):
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/attractions/{attractionId}"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching activity data: {response.status_code}")
        return None