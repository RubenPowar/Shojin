import googlemaps, math
from geopy.distance import geodesic



# Calculate the bearing between two points.
def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dLon = lon2 - lon1
    x = math.cos(lat2) * math.sin(dLon)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    initial_bearing = math.atan2(x, y)

    # Convert bearing from radians to degrees
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

# Convert a bearing to a cardinal direction.
def bearing_to_cardinal(bearing):
    cardinal_points = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West",
                       "North"]
    return cardinal_points[round(bearing / 45) % 8]

#Get the cardinal direction of the second location from the first.
def get_direction_between_points(lat1, lon1, lat2, lon2):
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    return bearing_to_cardinal(bearing)

def find_closest_centre(your_location, type):
    uk_cities_coordinates = {
        "London": {"latitude": 51.5074, "longitude": -0.1278},
        "Birmingham": {"latitude": 52.4862, "longitude": -1.8904},
        "Manchester": {"latitude": 53.4808, "longitude": -2.2426},
        "Glasgow": {"latitude": 55.8642, "longitude": -4.2518},
        "Edinburgh": {"latitude": 55.9533, "longitude": -3.1883},
        "Liverpool": {"latitude": 53.4084, "longitude": -2.9916},
        "Leeds": {"latitude": 53.8008, "longitude": -1.5491},
        "Bristol": {"latitude": 51.4545, "longitude": -2.5879},
        "Newcastle upon Tyne": {"latitude": 54.9783, "longitude": -1.6174},
        "Sheffield": {"latitude": 53.3811, "longitude": -1.4701},
        "Belfast": {"latitude": 54.5973, "longitude": -5.9301},
        "Cardiff": {"latitude": 51.4816, "longitude": -3.1791}
    }
    # your_location = (lat, long)
    closest_centre = None
    min_distance = None
    if type == 'city':
        list = uk_cities_coordinates
    for centre, coords in list.items():
        centre_location = (coords['latitude'], coords['longitude'])
        distance = geodesic(your_location, centre_location).kilometers

        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_centre = centre

    # prose = f"The closest {type} is {closest_centre} at coordinates {uk_cities_coordinates[closest_centre]}. "
    prose = f"The closest {type} is {closest_centre} . "

    prose += get_journey_prose(your_location, uk_cities_coordinates[closest_centre]['latitude'],
                      uk_cities_coordinates[closest_centre]['longitude'], 'city')

    return prose

def get_journey_prose(lat_long, destination_lat, destination_lng, destination_type):
    gmaps = googlemaps.Client(key='AIzaSyAUdmgR91R-qPfxS42g0UcExPZ9DadlFtw')
    prose = ''
    # Get driving directions to the destination
    directions_result = gmaps.directions(lat_long,
                                         (destination_lat, destination_lng),
                                         mode='driving')

    if directions_result:
        drive_distance = directions_result[0]['legs'][0]['distance']['text']
        drive_duration = directions_result[0]['legs'][0]['duration']['text']

        prose += f"It is a {drive_distance} drive "
        prose += f"(circa {drive_duration})"

    # else:
    # print("Could not retrieve driving information.")
    # Get walking directions to the destination
    directions_result = gmaps.directions(lat_long,
                                         (destination_lat, destination_lng),
                                         mode='walking')

    if directions_result and destination_type != 'major_airport':
        walk_distance = directions_result[0]['legs'][0]['distance']['text']
        walk_duration = directions_result[0]['legs'][0]['duration']['text']

        prose += f", or a {walk_distance} walk"
        prose += f" (circa {walk_duration})"

    directions_result = gmaps.directions(lat_long,
                                         (destination_lat, destination_lng),
                                         mode='transit')

    if directions_result:
        transit_duration = directions_result[0]['legs'][0]['duration']['text']

        prose += f" and circa {transit_duration} by public transport."
    else:
        prose += '.'
    return prose

def find_closest_destination_and_drive_info(api_key, location, destination_type):
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Define search keyword based on the destination type
    if destination_type == 'major_airport':
        keyword = 'international airport'
    elif destination_type == 'train_or_metro_station':
        keyword = 'train station|metro station|subway station|underground station|tube station|train|overground|rail'
    else:
        print("Invalid destination type. Choose 'airport', or 'train_metro_station'.")
        return

    # Use the Places API to search for the destination near the given location
    if destination_type != 'major_airport':
        places_result = gmaps.places_nearby(location=location, type='point_of_interest', keyword=keyword, rank_by='distance')
    else:
        places_result = gmaps.places_nearby(location=location, radius=50000, type='point_of_interest', keyword=keyword)

    if places_result['results']:
        closest_destination = places_result['results'][0]
        destination_name = closest_destination['name']
        destination_location = closest_destination['geometry']['location']
        destination_lat = destination_location['lat']
        destination_lng = destination_location['lng']

        # Calculate the geodesic distance
        geodesic_distance = geodesic(location, (destination_lat, destination_lng)).kilometers
        # Calculate bearing
        direction = get_direction_between_points(location[0], location[1], destination_lat, destination_lng)

        prose = ''
        prose += f"The closest {destination_type.replace('_', ' ')} is {destination_name}, "
        # print(f"Location: Latitude {destination_lat}, Longitude {destination_lng}")
        prose += f"{geodesic_distance:.2f} km {direction}. "
        # print(prose)

        # Get driving directions to the destination
        prose += get_journey_prose(location, destination_lat, destination_lng, destination_type)
        # Get driving directions to the destination
        # directions_result = gmaps.directions(location,
        #                                      (destination_lat, destination_lng),
        #                                      mode="driving")
        #
        # if directions_result:
        #     drive_distance = directions_result[0]['legs'][0]['distance']['text']
        #     drive_duration = directions_result[0]['legs'][0]['duration']['text']
        #
        #     prose += f"It is a {drive_distance} drive "
        #     prose += f"(circa {drive_duration})"
        #
        # # else:
        #     # print("Could not retrieve driving information.")


        # Get walking directions to the destination
        # # Get walking directions to the destination
        # directions_result = gmaps.directions(location,
        #                                     (destination_lat, destination_lng),
        #                                     mode="walking")
        #
        # if directions_result and destination_type == 'train_or_metro_station':
        #     walk_distance = directions_result[0]['legs'][0]['distance']['text']
        #     walk_duration = directions_result[0]['legs'][0]['duration']['text']
        #
        #     prose += f", or a {walk_distance} walk"
        #     prose += f" (circa {walk_duration})."
        # else:
        #     prose += '.'
        return prose
    else:
        return f"No {destination_type.replace('_', ' ')} found within the specified radius."

def generate_nearest_info(location):
    api_key = 'AIzaSyAUdmgR91R-qPfxS42g0UcExPZ9DadlFtw'
    prose = ''

    prose += find_closest_centre(location, 'city') + '\n'
    # print(f"The closest city is {closest_city} at coordinates {city_coords}.")


    # To find the closest international airport
    prose += find_closest_destination_and_drive_info(api_key, location, 'major_airport') + '\n'

    # To find the closest train or metro station
    prose += find_closest_destination_and_drive_info(api_key, location, 'train_or_metro_station') + '\n'

    return prose


if __name__ == '__main__':
    coordinates = (51.533214, -0.140666)  # Example location
    text = generate_nearest_info(coordinates)


    print(text)