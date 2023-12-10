import utilities
from datetime import datetime, timedelta
import Route_Point
import folium
import accidents_backend


def closeness_2_points_weight(accident,
                              route_point):  # returns the weights of distance by assumptions: 2 for vcery lose, 1 for close and 0 for far
    distance = utilities.distance_2_points(accident[0], accident[1], route_point[0], route_point[1])
    if distance > 400:
        return 0
    if distance > 200:
        return 1
    return 2


def time_diff_weight(accident,
                     route_point):  # returns weight of different in days between route and accident + different of time within the day
    time_route = route_point[3].time()
    time_accident = accident[2].time()
    date_route = route_point[3].date()
    date_accident = accident[2].date()

    delta_route = timedelta(hours=time_route.hour, minutes=time_route.minute, seconds=time_route.second)
    delta_accident = timedelta(hours=time_accident.hour, minutes=time_accident.minute, seconds=time_accident.second)

    dtime_days = abs((date_route - date_accident).days)
    dtime_seconds = abs((delta_accident - delta_route).total_seconds())

    if dtime_seconds > 3600:
        daytime_weight = 0
    elif dtime_seconds > 1200:
        daytime_weight = 1
    else:
        daytime_weight = 2

    if dtime_days > 730:
        days_weight = 0
    elif dtime_days > 365:
        days_weight = 1
    else:
        days_weight = 2

    total_weight = days_weight + daytime_weight

    return total_weight


def days_between_2_occasions(accident, route_point):  # returns how many days are between 2 occasions
    date_route = route_point[3].date()
    date_accident = accident[2].date()
    dtime_days = abs((date_route - date_accident).days)
    return dtime_days


def dangerous_cross_road_weight(accidents,
                                route_point):  # returns weighting of if a specific route point is a dangerous cross road
    accidents_in_radius_counter = 0
    for accident in accidents:
        distance = utilities.distance_2_points(accident[0], accident[1], route_point[0], route_point[1])
        time = days_between_2_occasions(accident, route_point)

        if distance <= 200 and time <= 365:
            accidents_in_radius_counter += 1

    if accidents_in_radius_counter <= 5:
        return 0
    if accidents_in_radius_counter <= 10:
        return 1
    return 2


def route_point_score(accidents, route_point):  # returns the total score of a route point
    score = 0
    for accident in accidents:
        time_score = time_diff_weight(accident, route_point)
        distance_score = closeness_2_points_weight(accident, route_point)
        score += time_score * distance_score  # if it's not dangerous by assumptions either time or distance, then it nulls
    cross_road_score = dangerous_cross_road_weight(accidents, route_point)
    score += cross_road_score
    return score


def draw_map(center_lat, center_lon, origin, destination, num_points, num_accidents, state):  # drawing a map and marking accidents and route point colored by its score
    map_center = [center_lat, center_lon]
    map = folium.Map(location=map_center, zoom_start=14)

    states = []

    tuppled_accidents = accidents_backend.get_accidents(num_accidents, state)

    routes_array_score, shareable_array = (mark_route_points(map, origin, destination, num_points, tuppled_accidents, states)[0],
                                         mark_route_points(map, origin, destination, num_points, tuppled_accidents, states)[1]) # marking route points on map and returns total score
    mark_accidents(map, tuppled_accidents, num_accidents, states) # marking accidents on map

    map.save("SafeJourney.html")

    best_route_num = evaluate_routes(routes_array_score)


    if best_route_num is not None and 0 <= best_route_num < len(routes_array_score):
        best_route_score = routes_array_score[best_route_num]
        best_route_link = shareable_array[best_route_num]
        print(f"all links are {shareable_array}")
        return best_route_score, best_route_link, best_route_num
    else:
        print("Error: Invalid best route number.")
        return None, None


def mark_route_points(map, origin, destination, num_points, accidents, states):
    number_routes = len(Route_Point.get_route(origin, destination, num_points)[0])
    score_array = []
    links_array = []
    for route_number in range(number_routes):
        route_points = Route_Point.get_route(origin, destination, num_points)[0][route_number]
        shareable_link = Route_Point.get_route(origin, destination, num_points)[1][route_number]
        timed_route_points = Route_Point.get_timed_route_points(route_points, num_points)  # adding the time stamps
        total_score = 0
        for index in range(0,num_points-2):  # loop through all route points
            lat, lon, time_point = timed_route_points[index][0], timed_route_points[index][1], timed_route_points[index][2]
            score = route_point_score(accidents, (lat, lon, index, time_point))  # scoring of route point
            color_route_point = 'green' if score < 50 else 'black'
            marker_icon_route_point = folium.Icon(color=color_route_point, icon='star')
            tooltip = "Point # " + str(index)
            folium.Marker([lat, lon], popup=str(index), tooltip=tooltip, icon=marker_icon_route_point).add_to(map)
            state = utilities.get_state(lat, lon)
            if state not in states:
                states.append(state)
            total_score += score
        score_array.append(total_score)
        links_array.append(shareable_link)

    return (score_array, links_array)


def mark_accidents(map, tuppled_accidents, num_accidents, states): #marks accidents in tuple formation [lat,lon,time]
    for index in range(int(num_accidents / 100)):  # loop through all route points & present some for visualization
        if tuppled_accidents[index][3] not in states:  # check if route point in relevant state
            continue
        lat, lon, timed = tuppled_accidents[index][0], tuppled_accidents[index][1], tuppled_accidents[index][2]
        color_accident_point = 'red'
        marker_icon_accident_point = folium.Icon(color=color_accident_point)
        tooltip = "Accident # " + str(index)
        folium.Marker([lat, lon], popup=str(index), tooltip=tooltip, icon=marker_icon_accident_point).add_to(map)


def evaluate_routes(routes_array):
    print(f"all scores are {routes_array}")
    if not routes_array:
        print("Error: No routes available.")
        return None

    best_route_num = min(range(len(routes_array)), key=lambda i: routes_array[i])

    if best_route_num is None:
        print("Error: No valid best route number found.")
        return None

    return best_route_num


