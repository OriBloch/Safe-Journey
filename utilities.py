from math import radians, sin, cos, sqrt, atan2
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time
import re


def distance_2_points(lat1, lon1, lat2, lon2):  # based on Haversine equation
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of the Earth in kilometers (mean value)
    R = 6371.0

    # Calculate the distance
    distance = R * c

    return distance * 1000  # return in meters


# def get_state_by_address(address):
#     geolocator = Nominatim(user_agent="my_geocoder")
#     location = geolocator.geocode(address)
#     if location:
#         state = location.raw.get('address', {}).get('state')
#         return state
#     else:
#         return None

def get_state_from_address(address):
    # Define a regular expression to match common state abbreviations or names
    state_regex = re.compile(
        r'\b(?:Colorado|CO)\b',flags=re.IGNORECASE)

    # Try to find a match in the address
    match = state_regex.search(address)

    if match:
        return match.group(0)
    else:
        return None


def get_state(lat, lon):
    geolocator = Nominatim(user_agent="my_geocoder")
    coord = f"{lat}, {lon}"

    max_retries = 3
    retry_delay = 2  # seconds

    for retry in range(1, max_retries + 1): # exception handling
        try:
            location = geolocator.reverse(coord, exactly_one=True)
            if location:
                address = location.raw.get('address', {})
                state = address.get('state', '')
                abbrev_state = shorten_state(state)
                return abbrev_state
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Attempt {retry}/{max_retries} failed: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Increase delay exponentially

    print(f"All attempts failed. Unable to retrieve state.")
    return None


def shorten_state(long_state): # returns abbrev of country e.g.: CO for Colorado
    abbrevs = {
        'AA': 'Armed Forces Americas',
        'AB': 'Alberta',
        'AE': 'Armed Forces Europe',
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AP': 'Armed Forces Pacific',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'BC': 'British Columbia',
        'CA': 'California',
        'CD': 'Canada',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'Dist. Of Columbia',
        'DE': 'Delaware',
        'FF': 'Foreign Countries',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MB': 'Manitoba',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'MX': 'Mexico',
        'NB': 'New Brunswick',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NL': 'Newfoundland and Labrador',
        'NM': 'New Mexico',
        'NS': 'Nova Scotia',
        'NT': 'Northwest Territories',
        'NU': 'Nunavut',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'ON': 'Ontario',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PE': 'Prince Edward Island',
        'PR': 'Puerto Rico',
        'QC': 'Quebec',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'SK': 'Saskatchewan',
        'TN': 'Tennessee',
        'TT': 'Trust Territory',
        'TX': 'Texas',
        'UN': 'Unknown',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming',
        'YT': 'Yukon ',
    }
    for abbrev_state, state in abbrevs.items():
        if state == long_state:
            return abbrev_state
    return None



