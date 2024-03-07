import googlemaps
import pandas as pd
import time, os
from geopy.distance import geodesic
from dotenv import load_dotenv

def as_the_crow_flies(c1, c2):
    distance_meters = int(geodesic(coords_1, coords_2).meters)
    return round(distance_meters / 1000, 1)

def journey_length(c1, c2, api_key, mode):
    gmaps = googlemaps.Client(key=api_key)

    # Making a request for walking directions
    directions_result = gmaps.directions(c1,
                                         c2,
                                         mode=mode)

    # Extracting the distance in meters from the directions result
    # Note: This assumes the first route and leg returned is the one we want
    try:
        walking_distance_meters = directions_result[0]['legs'][0]['distance']['value']
        walking_duration_seconds = directions_result[0]['legs'][0]['duration']['value']
    except:
        walking_distance_meters = 0
        walking_duration_seconds = 0
    return round(walking_distance_meters / 1000, 1), round(walking_duration_seconds / 60)

def get_journeys(c1, c2, api_key):
    distance = as_the_crow_flies(c1, c2)
    print(f"Between {c1} and {c2} :")
    print(f"Geodesic Distance: {distance} Kilometers")
    walking_distance, walking_time = journey_length(c1, c2, api_key, "walking")
    driving_distance, driving_time = journey_length(c1, c2, api_key, "driving")
    transit_distance, transit_time = journey_length(c1, c2, api_key, "transit")
    print(f"Walking Distance: {walking_distance} Kilometers, and {walking_time} minutes")
    print(f"Driving Distance: {driving_distance} Kilometers, and {driving_time} minutes")
    print(f"Transit Distance: {transit_distance} Kilometers, and {transit_time} minutes")


def generate_maps_info(location, filepath, api_key):
    map_client = googlemaps.Client(api_key)

    types = 'supermarket', 'doctor', 'movie_theater', 'park', 'primary_school', 'secondary_school', 'train_station', 'museum', 'shopping_mall'
    radius = 1
    distance = radius * 1000
    prose = ""

    for type in types:
        business_list = []

        response = map_client.places_nearby(
            location=location,
            type=type,
            radius=distance
        )

        business_list.extend(response.get('results'))
        next_page_token = response.get('next_page_token')

        while next_page_token:
            time.sleep(2)
            response = map_client.places_nearby(
                location=location,
                type=type,
                radius=distance,
                page_token=next_page_token
            )
            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

        df = pd.DataFrame(business_list)
        prose += ('There are '+ str(len(business_list))+ ' '+ type+ 's within '+ str(radius)+ 'km' + '\n')
        # df['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df['place_id']
        df.to_excel(filepath + 'MapsXLS/' + type + '.xlsx', index = False)
    return prose

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('GMAPS_API_KEY')
    coords_1 = (51.533214, -0.140666)  # Mornington Crescent
    coords_2 = (51.479618318306926, -0.33519562144767723)  # Heathrow Airport
    print(generate_maps_info(coords_1, '/Users/ruben/PycharmProjects/Shojin/files/MapsInfo/', api_key))

    get_journeys(coords_1, coords_2, api_key)



# https://developers.google.com/maps/documentation/places/web-service/search-nearby#location