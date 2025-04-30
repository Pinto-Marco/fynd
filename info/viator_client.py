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


def fetch_viator_availability_schedules(productCode):
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/availability/schedules/{productCode}"
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

def fetch_viator_destinations():
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/destinations"
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

# TODO add body to the request
def fetch_viator_free_text_search():
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/search/freetext"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    
    body = {
        'searchTerm': 'Rome', #stringa di ricerca
        'productFiltering' : {
            # un sacco di parametri
        },
        'productSorting' : {
            'sort': 'DEFAULT', # "ITINERARY_DURATION" "PRICE" "REVIEW_AVG_RATING" "DATE_ADDED"
            'order': 'DESCENDING' # "ASCENDING" "DESCENDING"
        },
        'searchTypes': [
            {
                'searchType': 'DESTINATION', # "PRODUCTS" "DESTINATIONS" "ATTRACTIONS"
                'pagination':  {
                    'start': 1,
                    'count': 10
                }
            }
        ],
        #One of: "AUD", "BRL", "CAD", "CHF", "DKK", "EUR", "GBP", "HKD", "INR", "JPY", "NOK", "NZD", "SEK", "SGD", "TWD", "USD", "ZAR".
        'currency': 'EUR',
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching activity data: {response.status_code}")
        return None

# TODO add body to the request
def fetch_viator_locations_bulk():
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/locations/bulk"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    body = {
        "locations": [
            'LOC-6eKJ+or5y8o99Qw0C8xWyD7vmtNs0RJ3U9ULt/7PkhU=',
            # 'string'
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching activity data: {response.status_code}")
        return None

def fetch_viator_exchange_rates():
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/exchange-rates"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    body = {
        'sourceCurrencies': [
            'EUR',
            'GBP'
        ],
        'targetCurrencies': [
          'USD',
          'AUD',  
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching activity data: {response.status_code}")
        return None


# TODO add body to the request
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

# TODO add body to the request
def fetch_viator_attractions_search():
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/attractions/search"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    body = {
        'destinationId': 732,
        # DEFAULT
        # ALPHABETICAL
        # REVIEW_AVG_RATING
        # 'sorting': 'REVIEW_AVG_RATING',
        'pagination': {
            'start': 1,
            'count': 30
        },

    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching activity data: {response.status_code}")
        return None
