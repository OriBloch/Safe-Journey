google_maps_api = ""  # enter your personal google maps api key
from googlemaps import convert
import googlemaps
import utilities
import requests
import urllib.parse
from datetime import datetime, timedelta


def encode_coordinates(coordinates):
    return "|".join([f"{coord['lat']:.6f},{coord['lng']:.6f}" for coord in coordinates])

def get_route(origin, destination, num_points):
    gmaps = googlemaps.Client(key=google_maps_api)

    # calling the API to get directions
    directions_results = gmaps.directions(origin, destination, mode="driving")
    instructions = []
    all_routes_points = []
    all_polylines = []
    # Extracting the overview polyline from the directions result
    for route_number, directions_result in enumerate(directions_results):
        polyline_point = directions_result['overview_polyline']['points']
        all_polylines.append((polyline_point))
    for i in range(len(all_polylines)):
        coordinates = googlemaps.convert.decode_polyline(all_polylines[i])

        distance_matrix_result = gmaps.distance_matrix(origin, destination)  # google API for distance data
        route_distance = distance_matrix_result['rows'][0]['elements'][0].get('distance', {}).get('value', 0)  # total distance of travel in meters

        start_address = urllib.parse.quote(directions_result[i]['legs'][0]['start_address'])
        end_address = urllib.parse.quote(directions_result[i]['legs'][0]['end_address'])

        instruction = f'https://www.google.com/maps/dir/?api=1&origin={start_address}&destination={end_address}&travelmode=driving&dir_action=navigate'
        instructions.append(instruction)

        route_points = []
        current_distance = 0

        for coord_1, coord_2 in zip(coordinates, coordinates[1:]):
            lat1, lon1 = coord_1['lat'], coord_1['lng']
            lat2, lon2 = coord_2['lat'], coord_2['lng']

            segment_distance = utilities.distance_2_points(lat1, lon1, lat2, lon2)

            ratio = (current_distance + segment_distance) / route_distance
            new_lat = lat1 + ratio * (lat2 - lat1)
            new_lon = lon1 + ratio * (lon2 - lon1)
            route_points.append((new_lat, new_lon))
            current_distance += segment_distance

        # Add the destination point to the route
        route_points.append((coordinates[-1]['lat'], coordinates[-1]['lng']))
        all_routes_points.append(route_points)

    return (all_routes_points, instructions, route_number)
def get_route(origin, destination, num_points):
    gmaps = googlemaps.Client(key=google_maps_api)

    # calling the API to get directions
    directions_results = gmaps.directions(origin, destination, mode="driving", alternatives=True)
    print("Number of routes:", len(directions_results))

    instructions = []
    all_routes_points = []

    for route_number, directions_result in enumerate(directions_results):
        # Extracting information for each route
        start_address = directions_result['legs'][0]['start_address']
        end_address = directions_result['legs'][0]['end_address']

        start_address_encoded = urllib.parse.quote(start_address)
        end_address_encoded = urllib.parse.quote(end_address)

        instruction = f'https://www.google.com/maps/dir/?api=1&origin={start_address_encoded}&destination={end_address_encoded}&travelmode=driving&dir_action=navigate'
        instruction += f'&dirflag={route_number + 1}'

        instructions.append(instruction)

        # Extracting coordinates for each route
        polyline_point = directions_result['overview_polyline']['points']
        coordinates = googlemaps.convert.decode_polyline(polyline_point)

        route_points = [(coord['lat'], coord['lng']) for coord in coordinates]
        all_routes_points.append(route_points)

    return all_routes_points, instructions


def get_timed_route_points(route_points, num_points):
    current_time = datetime.now()
    accumulated_time = timedelta(0)  # total time driven so far
    timed_route_points = []
    timed_route_point = (route_points[0][0], route_points[0][1], current_time)
    timed_route_points.append(timed_route_point)

    for index in range(1, num_points):
        traveled_time = travel_time(route_points[index - 1], route_points[index])

        if traveled_time:
            accumulated_time += traveled_time
            calculated_time = current_time + accumulated_time
            timed_route_point = (route_points[index][0], route_points[index][1], calculated_time)
            timed_route_points.append(timed_route_point)
        else:
            print(f"No valid travel time for segment {index}")

    return timed_route_points


def travel_time(origin, destination):
    base_url = 'https://maps.googleapis.com/maps/api/directions/json?'

    # Convert (lat, lon) coordinates to string format
    origin_str = f"{origin[0]},{origin[1]}"
    destination_str = f"{destination[0]},{destination[1]}"

    params = {
        'origin': origin_str,
        'destination': destination_str,
        'mode': 'driving',
        'key': google_maps_api,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'routes' in data and data['routes']:
        # Check if there are valid routes
        route = data['routes'][0]
        if 'legs' in route and route['legs']:
            # Extracting the time travel from the API response
            travel_time_seconds = route['legs'][0]['duration']['value']
            travel_time = timedelta(seconds=travel_time_seconds)
            return travel_time
        else:
            print(f"No valid travel time for segment from {origin} to {destination}")
    else:
        print(f"No valid routes found in the API response.")

    return None


