import requests
from django.conf import settings


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
def fetch_viator_free_text_search(body):
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/search/freetext"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    
    body_example = {
        'searchTerm': 'Aperitivo', # required stringa di ricerca
        "productFiltering": {
            "destination": "802",
        #     "dateRange": {
        #     "from": "2023-01-01", #  ISO-8601 (YYYY-MM-DD)
        #     "to": "2023-01-31" # ISO-8601 (YYYY-MM-DD)
        #     },
        #     "price": {
        #         "from": 0, # >= 0
        #         "to": 1000 # >= 0.01
        #     },
        #     "rating": {
        #         "from": 0, # >= 0
        #         "to": 5 # >= 0.01
        #     },
        #     "durationInMinutes": {
        #         "from": 0, # >= 0
        #         "to": 1000 # >= 1
        #     },
        #     "tags": [
        #         21972
        #     ],
        #     "flags": [
        #         "LIKELY_TO_SELL_OUT" # "NEW_ON_VIATOR", "SKIP_THE_LINE", "PRIVATE_TOUR", "LIKELY_TO_SELL_OUT"
        #     ],
        #     "includeAutomaticTranslations": true
        # },
        # 'productSorting' : {
        #     'sort': 'DEFAULT', # "ITINERARY_DURATION" "PRICE" "REVIEW_AVG_RATING" "DATE_ADDED"
        #     'order': 'DESCENDING' # "ASCENDING" "DESCENDING"
        },
        'searchTypes': [ # required
            {
                'searchType': 'PRODUCTS', # "PRODUCTS" "DESTINATIONS" "ATTRACTIONS"
                'pagination':  {
                    'start': 1, # >= 1
                    'count': 50 # [ 1.. 50 ] default 10
                }
            }
        ],
        #One of: "AUD", "BRL", "CAD", "CHF", "DKK", "EUR", "GBP", "HKD", "INR", "JPY", "NOK", "NZD", "SEK", "SGD", "TWD", "USD", "ZAR".
        'currency': 'EUR',  # required
    }
    response = requests.post(url, headers=headers, json=body_example)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching activity data: {response.status_code}")
        return None

# TODO add body to the request
def fetch_viator_locations_bulk(body):
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/locations/bulk"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    body_example = {
        "locations": [ # required array of strings, max 500
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

def fetch_viator_exchange_rates(body):
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/exchange-rates"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    body_example = {
        "sourceCurrencies": [ # required?
            "AUD",
            "EUR",
            "USD",
            "GBP"   
        ],
        "targetCurrencies": [ # required?
            "AUD",
            "EUR",
            "USD",
            "GBP"
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
def fetch_viator_products_search(body):
    
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
    body_example = {
        "filtering": { # required
            "destination": "802", # required
            # "tags": [
            # "<integer>",
            # "<integer>"
            # ],
            # "flags": [ 
            # "SPECIAL_OFFER", # "NEW_ON_VIATOR", "FREE_CANCELLATION", "SKIP_THE_LINE", "PRIVATE_TOUR", "SPECIAL_OFFER", "LIKELY_TO_SELL_OUT"
            # ],
            # "confirmationType": "<string>", # "INSTANT"
            # "rating": {
            # "from": "<integer>", >= 0
            # "to": "<integer>" >= 1
            # },
            # "durationInMinutes": {  
            # "from": "<integer>", >= 0
            # "to": "<integer>" >= 1
            # },
            # "includeAutomaticTranslations": true,
            # "attractionId": "<integer>",
            # "lowestPrice": "<number>", >= 0
            # "highestPrice": "<number>", > 0
            # "startDate": "<date>", ISO-8601 (YYYY-MM-DD)
            # "endDate": "<date>" ISO-8601 (YYYY-MM-DD)
        },
        "currency": "EUR",  # required "AUD", "BRL", "CAD", "CHF", "DKK", "EUR", "GBP", "HKD", "INR", "JPY", "NOK", "NZD", "SEK", "SGD", "TWD", "USD", "ZAR"
        "sorting": {
            "sort": "TRAVELER_RATING", # "DEFAULT", "PRICE", "TRAVELER_RATING", "ITINERARY_DURATION", "DATE_ADDED"
            "order": "DESCENDING"  # "ASCENDING", "DESCENDING"
        },
        "pagination": { 
            "start": 2, # >= 1
            "count": 50 # [ 1 .. 50 ] default 10
        }
    }
    #     {
    #   "filtering": {
    #     "destination": "732",
    #     "tags": [
    #       21972
    #     ],
    #     "flags": [
    #       "LIKELY_TO_SELL_OUT",
    #       "FREE_CANCELLATION"
    #     ],
    #     "lowestPrice": 5,
    #     "highestPrice": 500,
    #     "startDate": "2023-01-30",
    #     "endDate": "2023-02-28",
    #     "includeAutomaticTranslations": true,
    #     "confirmationType": "INSTANT",
    #     "durationInMinutes": {
    #       "from": 20,
    #       "to": 360
    #     },
    #     "rating": {
    #       "from": 3,
    #       "to": 5
    #     }
    #   },
    #   "sorting": {
    #     "sort": "TRAVELER_RATING",
    #     "order": "DESCENDING"
    #   },
    #   "pagination": {
    #     "start": 1,
    #     "count": 5
    #   },
    #   "currency": "USD"
    # }

    response = requests.post(url, headers=headers, json=body_example)
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
def fetch_viator_attractions_search(body):
    VIATOR_API_URL = settings.VIATOR_API_URL
    VIATOR_API_KEY = settings.VIATOR_API_KEY
    url = f"{VIATOR_API_URL}/attractions/search"
    headers = {
        'exp-api-key': f'{VIATOR_API_KEY}',
        'Accept': 'application/json;version=2.0',
        'Content-Type': 'application/json',
        'Accept-Language': 'it',
    }
    body_example = {
        'destinationId': 732,
        # DEFAULT ALPHABETICAL REVIEW_AVG_RATING
        # 'sorting': 'REVIEW_AVG_RATING',
        'pagination': {
            'start': 1, # >= 1
            'count': 10 # [ 1 .. 30 ] default 30
        },

    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching activity data: {response.status_code}")
        return None
